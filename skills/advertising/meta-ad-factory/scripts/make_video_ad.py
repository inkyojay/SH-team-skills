#!/usr/bin/env python3
"""Kling AI Image-to-Video — 메타 영상 광고 자동 생성기

원본 소스 이미지 하나를 Kling AI에 넣어 9:16 MP4 클립을 만든 뒤
output/.../video/ 폴더에 저장합니다.

사전 설정:
    export KLING_ACCESS_KEY="your-access-key"
    export KLING_SECRET_KEY="your-secret-key"

사용법:
    # CDN 이미지
    python3 make_video_ad.py --image "https://cdn.../hero.webp" --slug abc-bed-live

    # 로컬 이미지
    python3 make_video_ad.py --image "/path/to/hero.webp" --slug abc-bed-live

    # 프롬프트·모델·시간 지정
    python3 make_video_ad.py \\
        --image "https://..." \\
        --slug abc-bed-live \\
        --prompt "cinematic slow zoom, warm golden hour lighting" \\
        --duration 10 \\
        --model kling-v2-master \\
        --ratio 9:16

    # 1:1 피드용
    python3 make_video_ad.py --image "https://..." --slug abc-bed-live --ratio 1:1
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import hmac
import json
import os
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

# ── 출력 경로 ──────────────────────────────────────────────────────────────────
OUTPUT_BASE = Path("/Users/inkyo/Projects/team-skills/output/광고카피/sundayhug-meta-bulk")
SCRIPTS_DIR = Path(__file__).resolve().parent

# ── Kling API 기본값 ───────────────────────────────────────────────────────────
KLING_BASE = "https://api.klingai.com"
DEFAULT_MODEL = "kling-v1-6"
DEFAULT_DURATION = 5       # 5 또는 10 (초)
DEFAULT_RATIO = "9:16"     # 9:16 | 1:1 | 16:9
DEFAULT_CFG = 0.5
DEFAULT_MODE = "std"       # std | pro

# ratio → 기본 프롬프트
RATIO_PROMPTS = {
    "9:16": (
        "cinematic vertical video, gentle slow camera zoom in, "
        "soft warm lifestyle lighting, product photography feel, "
        "smooth motion, clean aesthetic"
    ),
    "1:1": (
        "cinematic square video, gentle camera drift, "
        "warm soft lighting, product lifestyle feel, smooth motion"
    ),
    "4:5": (
        "cinematic portrait video, gentle slow zoom, "
        "warm natural lighting, Instagram lifestyle feel, smooth motion"
    ),
    "16:9": (
        "cinematic landscape video, slow pan, "
        "warm lifestyle lighting, clean product aesthetic"
    ),
}


# ── JWT 생성 (PyJWT 없이 stdlib만 사용) ───────────────────────────────────────

def _b64url(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode()


def make_jwt(access_key: str, secret_key: str) -> str:
    """HS256 JWT 토큰 생성 (Kling API용). 유효 시간 30분."""
    now = int(time.time())
    header = _b64url(json.dumps({"alg": "HS256", "typ": "JWT"}).encode())
    payload = _b64url(json.dumps({
        "iss": access_key,
        "exp": now + 1800,
        "nbf": now - 5,
    }).encode())
    msg = f"{header}.{payload}"
    sig = _b64url(
        hmac.new(secret_key.encode(), msg.encode(), hashlib.sha256).digest()
    )
    return f"{msg}.{sig}"


# ── 이미지 처리 ───────────────────────────────────────────────────────────────

def image_to_value(image: str) -> tuple[str, str]:
    """이미지 경로/URL → (image_field_value, display_name).

    - CDN URL → URL 그대로 전송
    - 로컬 파일 → base64 data URI로 변환 (Kling API 허용)
    """
    if image.startswith(("http://", "https://")):
        return image, Path(image).name
    # 로컬 파일
    p = Path(image).resolve()
    if not p.exists():
        raise FileNotFoundError(f"이미지 파일을 찾을 수 없습니다: {p}")
    suffix = p.suffix.lower().lstrip(".")
    mime = {"jpg": "image/jpeg", "jpeg": "image/jpeg",
            "png": "image/png", "webp": "image/webp"}.get(suffix, "image/jpeg")
    b64 = base64.b64encode(p.read_bytes()).decode()
    return f"data:{mime};base64,{b64}", p.name


# ── Kling API 호출 ─────────────────────────────────────────────────────────────

def _api(method: str, path: str, token: str, body: dict | None = None) -> dict:
    url = f"{KLING_BASE}{path}"
    data = json.dumps(body).encode() if body else None
    req = urllib.request.Request(
        url, data=data, method=method,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        body_txt = e.read().decode(errors="replace")
        raise RuntimeError(f"Kling API 오류 {e.code}: {body_txt}") from e


def create_video_task(
    token: str,
    image_value: str,
    prompt: str,
    model: str,
    duration: int,
    ratio: str,
    mode: str,
    cfg_scale: float,
) -> str:
    """이미지→비디오 태스크 생성 → task_id 반환."""
    payload = {
        "model_name": model,
        "image": image_value,
        "prompt": prompt,
        "cfg_scale": cfg_scale,
        "mode": mode,
        "duration": str(duration),
        "aspect_ratio": ratio,
    }
    resp = _api("POST", "/v1/videos/image2video", token, payload)
    if resp.get("code", 200) != 200:
        raise RuntimeError(f"태스크 생성 실패: {resp}")
    task_id = resp.get("data", {}).get("task_id") or resp.get("task_id")
    if not task_id:
        raise RuntimeError(f"task_id 없음: {resp}")
    return task_id


def poll_task(token: str, task_id: str, max_wait: int = 300) -> str:
    """완료될 때까지 폴링 → 비디오 URL 반환."""
    deadline = time.time() + max_wait
    interval = 4
    print(f"  ⏳ 폴링 중 (최대 {max_wait}초)...", end="", flush=True)
    while time.time() < deadline:
        resp = _api("GET", f"/v1/videos/image2video/{task_id}", token)
        data = resp.get("data", resp)
        status = data.get("task_status", "")
        if status == "succeed":
            print(" ✓")
            videos = data.get("task_result", {}).get("videos", [])
            if not videos:
                raise RuntimeError("비디오 URL 없음")
            return videos[0]["url"]
        if status == "failed":
            raise RuntimeError(f"Kling 태스크 실패: {data}")
        print(".", end="", flush=True)
        time.sleep(interval)
    raise TimeoutError(f"타임아웃 {max_wait}초 초과")


def download_video(url: str, dest: Path) -> None:
    """비디오 URL → 로컬 파일 다운로드."""
    dest.parent.mkdir(parents=True, exist_ok=True)
    print(f"  📥 다운로드 중: {dest.name}")
    urllib.request.urlretrieve(url, dest)


# ── 메인 ──────────────────────────────────────────────────────────────────────

def find_output_dir(slug: str) -> Path:
    """slug 기반으로 output 폴더 자동 탐색."""
    matches = list(OUTPUT_BASE.glob(f"*/{slug}"))
    if matches:
        return matches[0]
    # events 서브폴더도 탐색
    matches = list(OUTPUT_BASE.glob(f"events/{slug}"))
    if matches:
        return matches[0]
    return OUTPUT_BASE / "misc" / slug


def main() -> None:
    ap = argparse.ArgumentParser(
        description="Kling AI image-to-video 메타 광고 생성기",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    ap.add_argument("--image", "-i", required=True,
                    help="이미지 URL 또는 로컬 파일 경로")
    ap.add_argument("--slug", "-s", required=True,
                    help="제품/이벤트 슬러그 (출력 폴더명)")
    ap.add_argument("--prompt", "-p", default=None,
                    help="영상 모션 프롬프트 (기본: 자동 선택)")
    ap.add_argument("--duration", "-d", type=int, default=DEFAULT_DURATION,
                    choices=[5, 10],
                    help=f"영상 길이 (초, 기본: {DEFAULT_DURATION})")
    ap.add_argument("--model", "-m", default=DEFAULT_MODEL,
                    help=f"Kling 모델 (기본: {DEFAULT_MODEL})")
    ap.add_argument("--ratio", "-r", default=DEFAULT_RATIO,
                    choices=["9:16", "1:1", "4:5", "16:9"],
                    help=f"영상 비율 (기본: {DEFAULT_RATIO})")
    ap.add_argument("--mode", default=DEFAULT_MODE,
                    choices=["std", "pro"],
                    help="생성 모드 (기본: std)")
    ap.add_argument("--cfg", type=float, default=DEFAULT_CFG,
                    help=f"CFG scale 0.0~1.0 (기본: {DEFAULT_CFG})")
    ap.add_argument("--output", "-o", default=None,
                    help="출력 파일 경로 (기본: 자동)")
    args = ap.parse_args()

    # ── API 키 확인 ────────────────────────────────────────────────────────────
    ak = os.environ.get("KLING_ACCESS_KEY", "")
    sk = os.environ.get("KLING_SECRET_KEY", "")
    if not ak or not sk:
        print("❌ 환경변수 KLING_ACCESS_KEY 와 KLING_SECRET_KEY 를 설정하세요.")
        print()
        print("  export KLING_ACCESS_KEY='your-access-key'")
        print("  export KLING_SECRET_KEY='your-secret-key'")
        sys.exit(1)

    # ── 프롬프트 결정 ──────────────────────────────────────────────────────────
    prompt = args.prompt or RATIO_PROMPTS.get(args.ratio, RATIO_PROMPTS["9:16"])

    # ── 이미지 처리 ────────────────────────────────────────────────────────────
    print(f"\n🎬 Kling Image-to-Video 시작")
    print(f"  이미지  : {args.image[:80]}{'...' if len(args.image) > 80 else ''}")
    print(f"  슬러그  : {args.slug}")
    print(f"  모델    : {args.model}")
    print(f"  비율    : {args.ratio}  길이: {args.duration}초")
    print(f"  프롬프트: {prompt[:80]}...")

    image_value, img_name = image_to_value(args.image)
    print(f"  이미지  : {'CDN URL' if args.image.startswith('http') else '로컬(base64)'}")

    # ── JWT 생성 ───────────────────────────────────────────────────────────────
    token = make_jwt(ak, sk)

    # ── 태스크 생성 ────────────────────────────────────────────────────────────
    print("  🚀 태스크 생성 중...")
    task_id = create_video_task(
        token=token,
        image_value=image_value,
        prompt=prompt,
        model=args.model,
        duration=args.duration,
        ratio=args.ratio,
        mode=args.mode,
        cfg_scale=args.cfg,
    )
    print(f"  🆔 task_id: {task_id}")

    # ── 폴링 ──────────────────────────────────────────────────────────────────
    video_url = poll_task(token, task_id)
    print(f"  🎥 비디오 URL: {video_url[:80]}...")

    # ── 저장 경로 결정 ─────────────────────────────────────────────────────────
    if args.output:
        dest = Path(args.output)
    else:
        out_dir = find_output_dir(args.slug)
        stem = Path(img_name).stem
        ratio_safe = args.ratio.replace(":", "x")
        dest = out_dir / "video" / f"{stem}_{args.duration}s_{ratio_safe}.mp4"

    # ── 다운로드 ───────────────────────────────────────────────────────────────
    download_video(video_url, dest)

    print(f"\n✅ 완료!")
    print(f"   저장 위치: {dest}")
    print(f"   Finder 열기: open \"{dest.parent}\"")


if __name__ == "__main__":
    main()
