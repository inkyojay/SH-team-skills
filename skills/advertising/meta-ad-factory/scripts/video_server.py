#!/usr/bin/env python3
"""로컬 영상 생성 서버 — preview-grid 🎬 버튼 원클릭 연동

preview-grid.html의 🎬 버튼이 이 서버로 요청을 보냄.
Kling API 또는 Mock(ffmpeg)으로 영상을 생성하고 결과를 반환.

사용법:
    python3 video_server.py          # 기본 포트 5173
    python3 video_server.py --mock   # Mock 모드 (ffmpeg, 크레딧 불필요)
    python3 video_server.py --port 8765

브라우저에서 http://localhost:5173 접속하면 상태 확인 가능.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import threading
import time
import uuid
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

PORT = 5173
SCRIPT_DIR = Path(__file__).resolve().parent
MAKE_VIDEO = SCRIPT_DIR / "make_video_ad.py"

# 진행 중인 작업 저장
jobs: dict[str, dict] = {}


def run_video_job(job_id: str, image: str, slug: str, ratio: str,
                  duration: int, mock: bool) -> None:
    """백그라운드 스레드에서 영상 생성 실행."""
    jobs[job_id]["status"] = "running"
    jobs[job_id]["log"] = []

    cmd = [sys.executable, str(MAKE_VIDEO),
           "--image", image,
           "--slug", slug,
           "--ratio", ratio,
           "--duration", str(duration)]
    if mock:
        cmd.append("--mock")

    env = os.environ.copy()
    try:
        proc = subprocess.Popen(
            cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
            text=True, env=env
        )
        output_lines = []
        for line in proc.stdout:
            line = line.rstrip()
            output_lines.append(line)
            jobs[job_id]["log"] = output_lines
            # 저장 경로 추출
            if "저장 위치" in line or "저장 위치" in line:
                parts = line.split(":", 1)
                if len(parts) > 1:
                    jobs[job_id]["dest"] = parts[1].strip()

        proc.wait()
        if proc.returncode == 0:
            jobs[job_id]["status"] = "done"
        else:
            jobs[job_id]["status"] = "error"
            jobs[job_id]["error"] = "\n".join(output_lines[-5:])
    except Exception as e:
        jobs[job_id]["status"] = "error"
        jobs[job_id]["error"] = str(e)


class Handler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):  # 기본 로그 억제
        pass

    def _send(self, code: int, data: dict) -> None:
        body = json.dumps(data, ensure_ascii=False).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):  # CORS preflight
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self):
        parsed = urlparse(self.path)

        # 상태 페이지
        if parsed.path == "/" or parsed.path == "":
            self._send(200, {
                "status": "running",
                "mode": "mock" if USE_MOCK else "kling",
                "jobs": len(jobs),
                "active": sum(1 for j in jobs.values() if j["status"] == "running"),
            })

        # 작업 상태 조회
        elif parsed.path.startswith("/status/"):
            job_id = parsed.path.split("/status/")[-1]
            job = jobs.get(job_id)
            if job:
                self._send(200, job)
            else:
                self._send(404, {"error": "job not found"})

        else:
            self._send(404, {"error": "not found"})

    def do_POST(self):
        if self.path != "/make-video":
            self._send(404, {"error": "not found"})
            return

        # 요청 바디 파싱
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length)
        try:
            req = json.loads(body)
        except Exception:
            self._send(400, {"error": "invalid JSON"})
            return

        image = req.get("image", "").strip()
        slug  = req.get("slug", "").strip()
        ratio = req.get("ratio", "9:16")
        duration = int(req.get("duration", 5))
        mock = req.get("mock", USE_MOCK)

        if not image or not slug:
            self._send(400, {"error": "image and slug are required"})
            return

        # 작업 등록 + 백그라운드 실행
        job_id = str(uuid.uuid4())[:8]
        jobs[job_id] = {
            "job_id": job_id,
            "status": "queued",
            "image": image[:80],
            "slug": slug,
            "ratio": ratio,
            "duration": duration,
            "mock": mock,
            "log": [],
            "dest": None,
            "error": None,
            "created_at": time.time(),
        }
        t = threading.Thread(
            target=run_video_job,
            args=(job_id, image, slug, ratio, duration, mock),
            daemon=True,
        )
        t.start()
        self._send(200, {"job_id": job_id, "status": "queued"})


def main() -> None:
    global USE_MOCK

    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--mock", action="store_true",
                    help="Mock 모드 (ffmpeg, Kling 크레딧 불필요)")
    ap.add_argument("--port", type=int, default=PORT,
                    help=f"포트 (기본: {PORT})")
    args = ap.parse_args()
    USE_MOCK = args.mock

    mode_label = "🧪 MOCK (ffmpeg)" if USE_MOCK else "🎬 KLING AI"
    print(f"\n{'='*50}")
    print(f"  영상 광고 로컬 서버  {mode_label}")
    print(f"{'='*50}")
    print(f"  URL  : http://localhost:{args.port}")
    print(f"  모드 : {mode_label}")
    if not USE_MOCK:
        ak = os.environ.get("KLING_ACCESS_KEY", "")
        if not ak:
            print(f"  ⚠️  KLING_ACCESS_KEY 없음 — --mock 모드 권장")
        else:
            print(f"  ✓  KLING_ACCESS_KEY 감지됨")
    print(f"\n  preview-grid 에서 🎬 버튼을 클릭하세요!")
    print(f"  종료: Ctrl+C\n")

    server = HTTPServer(("localhost", args.port), Handler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n\n서버 종료.")


if __name__ == "__main__":
    USE_MOCK = False
    main()
