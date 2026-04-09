# Lyria 3 API Quick Reference

## 모델 목록
| 모델 | ID | 길이 | 용도 |
|------|-----|------|------|
| Lyria 3 Clip | `lyria-3-clip-preview` | 30초 고정 | 쇼츠, 빠른 생성 |
| Lyria 3 Pro | `lyria-3-pro-preview` | ~3분 | 풀 트랙 |
| Lyria RealTime | `lyria-rt-preview` | 스트리밍 | 실시간 생성 |

## 기본 사용법 (Python)
```python
from google import genai
from google.genai import types

client = genai.Client()  # GOOGLE_API_KEY 환경변수 자동 사용

# 30초 클립 생성
response = client.models.generate_content(
    model="lyria-3-clip-preview",
    contents="Catchy K-pop song about baby sleep facts, 120 BPM, fun lyrics in Korean",
    config=types.GenerateContentConfig(
        response_modalities=["AUDIO", "TEXT"],
    )
)

# 오디오 추출
for part in response.candidates[0].content.parts:
    if hasattr(part, "inline_data") and part.inline_data.mime_type.startswith("audio/"):
        with open("output.mp3", "wb") as f:
            f.write(part.inline_data.data)
```

## 주요 기능
- **가사 자동 생성**: 프롬프트에 가사 없이 설명만 해도 자동 생성
- **가사 지정**: 프롬프트에 가사를 포함하면 해당 가사로 노래 생성
- **템포 조절**: "120 BPM", "fast tempo" 등 자연어로 지정
- **이미지→음악**: 이미지 업로드하면 분위기에 맞는 음악 생성
- **SynthID 워터마크**: 모든 출력에 자동 포함 (AI 생성 표시)

## 출력 형식
- 기본: MP3
- Pro: MP3 또는 WAV (`response_mime_type` 설정)
- 48kHz 스테레오

## 가격 (유료 티어 필요)
- Gemini API 유료 키 필요
- 정확한 가격은 https://ai.google.dev/pricing 확인
