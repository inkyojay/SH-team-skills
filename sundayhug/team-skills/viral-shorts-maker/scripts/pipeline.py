#!/usr/bin/env python3
"""
Viral Shorts Maker — 전체 파이프라인 오케스트레이터
주제 하나만 입력하면 가사 → 음악 → 장면 → 최종 영상까지 자동 생성.
"""

import argparse
import json
import os
import subprocess
import sys
import shutil
from pathlib import Path

# Import local modules
SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))

from lyrics_generator import generate_lyrics
from music_generator import generate_music_clip, generate_music_pro, STYLE_PRESETS
from scene_generator import generate_scenes


def check_prerequisites():
    """사전 요구사항 확인."""
    errors = []

    # Check API keys
    gemini_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if not gemini_key:
        errors.append("GEMINI_API_KEY 환경변수가 설정되지 않았습니다.")

    # Check Node.js
    if not shutil.which("node"):
        errors.append("Node.js가 설치되지 않았습니다.")

    # Check ffmpeg
    if not shutil.which("ffmpeg"):
        errors.append("ffmpeg가 설치되지 않았습니다.")

    # Check Python packages
    try:
        from google import genai
    except ImportError:
        errors.append("google-genai 패키지: pip install google-genai --break-system-packages")

    try:
        from google import genai
    except ImportError:
        errors.append("google-genai 패키지: pip install google-genai --break-system-packages")

    if errors:
        print("❌ 사전 요구사항 미충족:")
        for e in errors:
            print(f"   • {e}")
        return False

    print("✅ 사전 요구사항 확인 완료")
    return True


def setup_remotion_project(work_dir: Path):
    """Remotion 프로젝트 초기화 (없는 경우)."""
    remotion_dir = work_dir / "remotion"

    if (remotion_dir / "package.json").exists():
        print("✅ Remotion 프로젝트 존재")
        return remotion_dir

    print("📦 Remotion 프로젝트 초기화 중...")
    remotion_dir.mkdir(parents=True, exist_ok=True)

    # Create package.json
    package_json = {
        "name": "viral-shorts-remotion",
        "version": "1.0.0",
        "private": True,
        "scripts": {
            "start": "npx remotion studio",
            "render": "npx remotion render Main output.mp4"
        },
        "dependencies": {
            "remotion": "^4.0.0",
            "@remotion/cli": "^4.0.0",
            "@remotion/renderer": "^4.0.0",
            "react": "^18.0.0",
            "react-dom": "^18.0.0"
        },
        "devDependencies": {
            "typescript": "^5.0.0",
            "@types/react": "^18.0.0"
        }
    }

    with open(remotion_dir / "package.json", "w") as f:
        json.dump(package_json, f, indent=2)

    # Create tsconfig
    tsconfig = {
        "compilerOptions": {
            "target": "ES2022",
            "module": "commonjs",
            "jsx": "react-jsx",
            "strict": True,
            "esModuleInterop": True,
            "outDir": "./dist",
            "baseUrl": "."
        },
        "include": ["src/**/*"]
    }

    with open(remotion_dir / "tsconfig.json", "w") as f:
        json.dump(tsconfig, f, indent=2)

    # Create src directory
    src_dir = remotion_dir / "src"
    src_dir.mkdir(parents=True, exist_ok=True)

    # Create Root.tsx
    root_tsx = '''import { Composition } from "remotion";
import { Main } from "./Main";

export const RemotionRoot: React.FC = () => {
  return (
    <Composition
      id="Main"
      component={Main}
      durationInFrames={900}  // 30fps * 30sec
      fps={30}
      width={1080}
      height={1920}
      defaultProps={{
        dataPath: "../data/render_data.json",
      }}
    />
  );
};
'''
    with open(src_dir / "Root.tsx", "w") as f:
        f.write(root_tsx)

    # Create index.ts
    index_ts = '''import { registerRoot } from "remotion";
import { RemotionRoot } from "./Root";
registerRoot(RemotionRoot);
'''
    with open(src_dir / "index.ts", "w") as f:
        f.write(index_ts)

    # Create Main.tsx - the actual video composition
    main_tsx = '''import React from "react";
import {
  useCurrentFrame,
  useVideoConfig,
  Sequence,
  Audio,
  OffthreadVideo,
  Img,
  interpolate,
  spring,
} from "remotion";
import * as fs from "fs";
import * as path from "path";

interface Section {
  index: number;
  type: string;
  start_sec: number;
  end_sec: number;
  lyrics: string;
  video_path: string | null;
  image_path: string | null;
}

interface RenderData {
  title: string;
  music_path: string;
  scenes: Section[];
  subtitle_color: string;
  subtitle_bg_color: string;
  total_duration_sec: number;
}

interface MainProps {
  dataPath: string;
}

const Subtitle: React.FC<{ text: string; color: string; bgColor: string }> = ({
  text,
  color,
  bgColor,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const opacity = interpolate(frame % (fps * 0.5), [0, 5], [0, 1], {
    extrapolateRight: "clamp",
  });

  return (
    <div
      style={{
        position: "absolute",
        bottom: 120,
        left: 40,
        right: 40,
        display: "flex",
        justifyContent: "center",
      }}
    >
      <div
        style={{
          backgroundColor: bgColor,
          padding: "16px 24px",
          borderRadius: 12,
          opacity,
        }}
      >
        <p
          style={{
            color: color,
            fontSize: 42,
            fontWeight: "bold",
            textAlign: "center",
            margin: 0,
            lineHeight: 1.4,
            textShadow: "2px 2px 4px rgba(0,0,0,0.5)",
            whiteSpace: "pre-line",
          }}
        >
          {text}
        </p>
      </div>
    </div>
  );
};

const TitleCard: React.FC<{ title: string }> = ({ title }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const scale = spring({ frame, fps, config: { damping: 12, stiffness: 200 } });
  const opacity = interpolate(frame, [fps * 1.5, fps * 2], [1, 0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  return (
    <div
      style={{
        position: "absolute",
        inset: 0,
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        backgroundColor: "rgba(0,0,0,0.7)",
        opacity,
      }}
    >
      <h1
        style={{
          color: "#FFFFFF",
          fontSize: 64,
          fontWeight: "bold",
          textAlign: "center",
          transform: `scale(${scale})`,
          padding: "0 40px",
          lineHeight: 1.3,
        }}
      >
        {title}
      </h1>
    </div>
  );
};

export const Main: React.FC<MainProps> = ({ dataPath }) => {
  // In production, load from file. For dev, use default data.
  let data: RenderData;
  try {
    const raw = fs.readFileSync(path.resolve(dataPath), "utf-8");
    data = JSON.parse(raw);
  } catch {
    // Fallback for studio preview
    data = {
      title: "Sample Video",
      music_path: "",
      scenes: [],
      subtitle_color: "#FFFFFF",
      subtitle_bg_color: "#00000088",
      total_duration_sec: 30,
    };
  }

  const { fps } = useVideoConfig();

  return (
    <div style={{ flex: 1, backgroundColor: "#000" }}>
      {/* Background music */}
      {data.music_path && (
        <Audio src={data.music_path} volume={1} />
      )}

      {/* Title card */}
      <Sequence from={0} durationInFrames={fps * 2}>
        <TitleCard title={data.title} />
      </Sequence>

      {/* Scene clips with subtitles */}
      {data.scenes.map((scene, i) => {
        const startFrame = Math.round(scene.start_sec * fps);
        const durationFrames = Math.round((scene.end_sec - scene.start_sec) * fps);

        return (
          <Sequence key={i} from={startFrame} durationInFrames={durationFrames}>
            {/* Video or image background */}
            {scene.video_path ? (
              <OffthreadVideo
                src={scene.video_path}
                style={{
                  width: "100%",
                  height: "100%",
                  objectFit: "cover",
                }}
              />
            ) : scene.image_path ? (
              <Img
                src={scene.image_path}
                style={{
                  width: "100%",
                  height: "100%",
                  objectFit: "cover",
                }}
              />
            ) : (
              <div style={{ flex: 1, backgroundColor: "#1a1a2e" }} />
            )}

            {/* Subtitle overlay */}
            {scene.lyrics && (
              <Subtitle
                text={scene.lyrics}
                color={data.subtitle_color}
                bgColor={data.subtitle_bg_color}
              />
            )}
          </Sequence>
        );
      })}
    </div>
  );
};
'''
    with open(src_dir / "Main.tsx", "w") as f:
        f.write(main_tsx)

    # Install dependencies
    print("📦 npm 패키지 설치 중...")
    result = subprocess.run(
        ["npm", "install"],
        cwd=str(remotion_dir),
        capture_output=True,
        text=True,
        timeout=120,
    )

    if result.returncode != 0:
        print(f"⚠️ npm install 경고: {result.stderr[:200]}")

    print("✅ Remotion 프로젝트 초기화 완료")
    return remotion_dir


def render_video(remotion_dir: Path, render_data: dict, output_path: str):
    """Remotion으로 최종 영상을 렌더링한다."""
    # Save render data
    data_dir = remotion_dir / "data"
    data_dir.mkdir(exist_ok=True)

    data_path = data_dir / "render_data.json"
    with open(data_path, "w", encoding="utf-8") as f:
        json.dump(render_data, f, ensure_ascii=False, indent=2)

    print(f"\n🎬 최종 영상 렌더링 중...")
    print(f"   출력: {output_path}")

    fps = 30
    total_frames = int(render_data["total_duration_sec"] * fps)

    cmd = [
        "npx", "remotion", "render",
        "Main", output_path,
        f"--props={json.dumps({'dataPath': str(data_path)})}",
        f"--frames=0-{total_frames}",
    ]

    result = subprocess.run(
        cmd,
        cwd=str(remotion_dir),
        capture_output=True,
        text=True,
        timeout=300,
    )

    if result.returncode != 0:
        print(f"❌ 렌더링 실패:\n{result.stderr[:500]}")
        return False

    print(f"✅ 렌더링 완료: {output_path}")
    return True


def fallback_ffmpeg_render(music_path: str, scenes: list, output_path: str,
                           total_duration: int):
    """Remotion 실패 시 ffmpeg로 기본 합성."""
    print("\n🔧 ffmpeg 폴백 렌더링 중...")

    # Collect video/image files
    input_files = []
    for scene in scenes:
        if scene.get("video_path") and os.path.exists(scene["video_path"]):
            input_files.append(scene["video_path"])
        elif scene.get("image_path") and os.path.exists(scene["image_path"]):
            input_files.append(scene["image_path"])

    if not input_files:
        print("❌ 사용 가능한 장면 파일이 없습니다.")
        return False

    # Create concat file
    concat_path = "/tmp/concat_list.txt"
    with open(concat_path, "w") as f:
        for fpath in input_files:
            f.write(f"file '{os.path.abspath(fpath)}'\n")

    # Basic ffmpeg concat + audio merge
    cmd = ["ffmpeg", "-y"]

    if all(f.endswith(".mp4") for f in input_files):
        cmd += ["-f", "concat", "-safe", "0", "-i", concat_path]
    else:
        # For images, create slideshow
        dur_per = total_duration / len(input_files)
        cmd += ["-framerate", f"1/{dur_per}", "-pattern_type", "glob",
                "-i", f"{os.path.dirname(input_files[0])}/*.png"]

    if music_path and os.path.exists(music_path):
        cmd += ["-i", music_path, "-shortest"]

    cmd += [
        "-vf", "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2",
        "-c:v", "libx264", "-preset", "fast",
        "-c:a", "aac", "-b:a", "192k",
        "-t", str(total_duration),
        output_path,
    ]

    result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)

    if result.returncode == 0:
        print(f"✅ ffmpeg 렌더링 완료: {output_path}")
        return True
    else:
        print(f"❌ ffmpeg 렌더링 실패: {result.stderr[:300]}")
        return False


def run_pipeline(topic: str, style: str = "catchy-kpop",
                 duration: int = 30, output: str = "output.mp4",
                 scene_mode: str = "image-to-video",
                 music_model: str = "clip",
                 skip_prerequisites: bool = False):
    """전체 파이프라인을 실행한다."""

    print("=" * 60)
    print("🚀 Viral Shorts Maker — 파이프라인 시작")
    print("=" * 60)
    print(f"   주제: {topic}")
    print(f"   스타일: {style}")
    print(f"   길이: {duration}초")
    print(f"   출력: {output}")
    print("=" * 60)

    # Setup work directory
    work_dir = Path(output).parent
    work_dir.mkdir(parents=True, exist_ok=True)

    # Check prerequisites
    if not skip_prerequisites and not check_prerequisites():
        sys.exit(1)

    # Set GOOGLE_API_KEY from GEMINI_API_KEY
    if os.environ.get("GEMINI_API_KEY"):
        os.environ["GOOGLE_API_KEY"] = os.environ["GEMINI_API_KEY"]

    # ==========================================
    # Step 1: 가사 생성
    # ==========================================
    print("\n" + "=" * 60)
    print("📝 Step 1/4: 가사 + 장면 설명 생성")
    print("=" * 60)

    lyrics_data = generate_lyrics(topic, style, duration)
    lyrics_path = work_dir / "lyrics.json"
    with open(lyrics_path, "w", encoding="utf-8") as f:
        json.dump(lyrics_data, f, ensure_ascii=False, indent=2)

    # ==========================================
    # Step 2: 음악 생성
    # ==========================================
    print("\n" + "=" * 60)
    print("🎵 Step 2/4: AI 음악 생성")
    print("=" * 60)

    # Apply style preset
    if style in STYLE_PRESETS:
        lyrics_data["music_prompt"] = STYLE_PRESETS[style]

    music_path = work_dir / "music.mp3"
    try:
        if music_model == "pro":
            audio_bytes = generate_music_pro(lyrics_data)
        else:
            audio_bytes = generate_music_clip(lyrics_data)

        with open(music_path, "wb") as f:
            import base64
            if isinstance(audio_bytes, str):
                f.write(base64.b64decode(audio_bytes))
            else:
                f.write(audio_bytes)
        print(f"✅ 음악 저장: {music_path}")
    except Exception as e:
        print(f"⚠️ 음악 생성 실패 (계속 진행): {e}")
        music_path = None

    # ==========================================
    # Step 3: 장면 영상 생성
    # ==========================================
    print("\n" + "=" * 60)
    print("🎬 Step 3/4: AI 장면 영상 생성")
    print("=" * 60)

    scenes_dir = work_dir / "scenes"
    try:
        scene_files = generate_scenes(lyrics_data, str(scenes_dir), scene_mode)
    except Exception as e:
        print(f"⚠️ 장면 생성 실패: {e}")
        scene_files = []

    # ==========================================
    # Step 4: 최종 영상 합성
    # ==========================================
    print("\n" + "=" * 60)
    print("🎞️ Step 4/4: 최종 영상 합성")
    print("=" * 60)

    # Prepare render data
    render_data = {
        "title": lyrics_data.get("title", topic),
        "music_path": str(music_path) if music_path and music_path.exists() else "",
        "scenes": scene_files,
        "subtitle_color": lyrics_data.get("subtitle_color", "#FFFFFF"),
        "subtitle_bg_color": lyrics_data.get("subtitle_bg_color", "#00000088"),
        "total_duration_sec": lyrics_data.get("total_duration_sec", duration),
    }

    # Try Remotion first
    try:
        remotion_dir = setup_remotion_project(work_dir)
        success = render_video(remotion_dir, render_data, str(output))
    except Exception as e:
        print(f"⚠️ Remotion 렌더링 실패: {e}")
        success = False

    # Fallback to ffmpeg
    if not success:
        success = fallback_ffmpeg_render(
            str(music_path) if music_path else None,
            scene_files,
            str(output),
            duration,
        )

    # ==========================================
    # 완료
    # ==========================================
    print("\n" + "=" * 60)
    if success:
        file_size = os.path.getsize(output) / (1024 * 1024) if os.path.exists(output) else 0
        print(f"🎉 완료! 최종 영상: {output} ({file_size:.1f} MB)")
    else:
        print("⚠️ 최종 영상 렌더링에 실패했지만, 중간 결과물은 저장되었습니다:")
        print(f"   가사: {lyrics_path}")
        if music_path and music_path.exists():
            print(f"   음악: {music_path}")
        if scenes_dir.exists():
            print(f"   장면: {scenes_dir}/")
    print("=" * 60)

    return success


def main():
    parser = argparse.ArgumentParser(
        description="🚀 Viral Shorts Maker — 바이럴 쇼츠 자동 생성",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
사용 예시:
  python pipeline.py --topic "아기 수면 잡지식 5가지" --style catchy-kpop
  python pipeline.py --topic "커피의 놀라운 효과" --style lofi-chill --duration 60
  python pipeline.py --topic "고양이가 박스를 좋아하는 이유" --music-model pro

스타일 프리셋:
  catchy-kpop   밝고 중독성 있는 K-pop (기본)
  lofi-chill    잔잔한 로파이
  edm-hype      빠르고 에너지 넘치는 EDM
  acoustic-warm 따뜻한 어쿠스틱
  funky-groove  펑키한 그루브
  reggaeton-bounce 레게톤 바운스
        """
    )
    parser.add_argument("--topic", required=True, help="영상 주제")
    parser.add_argument("--style", default="catchy-kpop",
                        help="음악 스타일 프리셋 또는 커스텀 프롬프트")
    parser.add_argument("--duration", type=int, default=30,
                        help="목표 길이 (초, 기본: 30)")
    parser.add_argument("--output", default="output/shorts.mp4",
                        help="출력 파일 경로")
    parser.add_argument("--scene-mode", choices=["image-to-video", "text-to-video"],
                        default="image-to-video",
                        help="장면 생성 방식")
    parser.add_argument("--music-model", choices=["clip", "pro"],
                        default="clip",
                        help="clip=30초, pro=최대3분")
    parser.add_argument("--skip-prerequisites", action="store_true",
                        help="사전 요구사항 검사 건너뛰기")

    args = parser.parse_args()

    run_pipeline(
        topic=args.topic,
        style=args.style,
        duration=args.duration,
        output=args.output,
        scene_mode=args.scene_mode,
        music_model=args.music_model,
        skip_prerequisites=args.skip_prerequisites,
    )


if __name__ == "__main__":
    main()
