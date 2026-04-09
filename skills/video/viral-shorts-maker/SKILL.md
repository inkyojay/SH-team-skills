---
name: viral-shorts-maker
description: >
  바이럴 쇼츠 영상을 자동 생성하는 스킬. 주제만 입력하면 위트 있는 가사 생성, AI 음악 생성 (Google Lyria 3 Pro),
  장면 영상 생성 (Google Veo 3.1 + Nano Banana), Remotion으로 최종 영상 편집/렌더링까지 전체 파이프라인을 자동 실행한다.
  다음 상황에서 반드시 이 스킬을 사용한다 - 쇼츠 만들어줘, 바이럴 영상, 잡지식 노래 영상, 숏폼 콘텐츠,
  릴스 만들어줘, 음악 영상 자동 생성, AI 뮤직비디오, 노래로 콘텐츠 만들어줘, Lyria 음악 생성,
  Veo 영상 생성, Remotion 영상 편집 등 숏폼 영상 자동 생성 관련 요청 시.
---

# Viral Shorts Maker — 바이럴 쇼츠 자동 생성 파이프라인

## 개요
주제 하나만 입력하면 위트 있는 가사 → AI 음악 → AI 장면 영상 → 최종 편집까지 자동으로 쇼츠 영상을 생성하는 스킬.

## 파이프라인

```
주제 입력
  ↓
[Step 1] 가사 + 장면 설명 생성 (Claude)
  ↓
[Step 2] 음악 생성 (Google Lyria 3 Pro API)
  ↓
[Step 3] 장면 영상 생성 (Veo 3.1 + Nano Banana 2)
  ↓
[Step 4] Remotion으로 합성 + 렌더링
  ↓
최종 .mp4 출력 (9:16, 30초~1분)
```

## 사전 요구사항

### API 키
- **Google Gemini API Key**: Lyria 3 Pro + Veo 3.1 + Nano Banana 모두 이 하나의 키로 사용
  - 발급: https://aistudio.google.com/apikey
  - 유료 티어 필요 (Lyria, Veo는 paid preview)
  - 환경변수: `GEMINI_API_KEY`

### 시스템 요구사항
- Node.js 18+
- Python 3.10+
- ffmpeg (Remotion 렌더링용)
- Chrome/Chromium (Remotion 렌더링용)

## 사용법

### 전체 파이프라인 실행
```bash
cd skills/video/viral-shorts-maker
python scripts/pipeline.py \
  --topic "아기가 잠을 잘 자는 신기한 과학적 사실 5가지" \
  --style "catchy k-pop" \
  --duration 30 \
  --output ../../../output/영상/baby-sleep-facts.mp4
```

### 개별 단계 실행

```bash
# Step 1: 가사 생성만
python scripts/lyrics_generator.py --topic "아기 수면 잡지식" --output lyrics.json

# Step 2: 음악 생성만
python scripts/music_generator.py --lyrics lyrics.json --style "upbeat pop" --output music.mp3

# Step 3: 장면 생성만
python scripts/scene_generator.py --scenes lyrics.json --output scenes/

# Step 4: 영상 합성만
cd remotion-template && npx remotion render Main output.mp4 --props='{"music":"../music.mp3","scenes":"../scenes/"}'
```

## 상세 구현

### Step 1: 가사 + 장면 설명 생성

`scripts/lyrics_generator.py` 실행. Claude API로 주제에 맞는 가사를 생성한다.

**출력 JSON 구조:**
```json
{
  "title": "아기 수면의 비밀",
  "total_duration_sec": 30,
  "sections": [
    {
      "type": "verse",
      "start_sec": 0,
      "end_sec": 8,
      "lyrics": "아기는 하루에 열여섯 시간 자\n어른의 두 배야 놀랍지 않아",
      "scene_description": "귀여운 아기가 포근한 이불 속에서 평화롭게 잠든 모습, 시계가 16시간을 표시",
      "scene_style": "warm, soft lighting, nursery room, close-up"
    }
  ],
  "music_prompt": "Catchy upbeat K-pop with playful synth melody, 120 BPM, fun and educational vibe"
}
```

### Step 2: 음악 생성 (Lyria 3 Pro)

`scripts/music_generator.py` 실행. Google Gemini API의 Lyria 3 모델을 호출.

- **Lyria 3 Clip**: 30초 클립 (빠름, 쇼츠에 적합)
- **Lyria 3 Pro**: 최대 3분 (긴 콘텐츠용)
- 가사 포함 생성 지원 (time-aligned lyrics)
- 출력: MP3 또는 WAV (48kHz stereo)

### Step 3: 장면 영상 생성 (Veo 3.1)

`scripts/scene_generator.py` 실행. 각 가사 섹션별로:
1. Nano Banana 2로 키 이미지 생성
2. Veo 3.1로 8초 영상 클립 생성 (이미지 → 영상)
3. 9:16 세로 비율 (portrait) 지정

### Step 4: Remotion 합성

`remotion-template/` 프로젝트에서:
- 음악 트랙을 배경으로 배치
- 장면 클립들을 타임라인에 시퀀싱
- 가사 자막 오버레이 (하단 자막 스타일)
- 인트로/아웃로 텍스트 추가
- 9:16 1080x1920 렌더링

## 커스터마이징

### 음악 스타일 프리셋
- `catchy-kpop`: 밝고 중독성 있는 K-pop
- `lofi-chill`: 잔잔한 로파이
- `edm-hype`: 빠르고 에너지 넘치는 EDM
- `acoustic-warm`: 따뜻한 어쿠스틱

### 영상 스타일 프리셋
- `cartoon`: 일러스트/카툰풍
- `cinematic`: 시네마틱 실사풍
- `minimal`: 깔끔한 모션그래픽풍

## 참고
- Lyria API 문서: `references/lyria_api.md`
- Veo API 문서: `references/veo_api.md`
- Remotion 템플릿: `remotion-template/`
