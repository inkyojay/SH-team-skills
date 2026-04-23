# Veo 3.1 API Quick Reference

## 모델 목록
| 모델 | ID | 비용 | 용도 |
|------|-----|------|------|
| Veo 3.1 | `veo-3.1-generate-preview` | 프리미엄 | 최고 품질, 네이티브 오디오 |
| Veo 3.1 Fast | `veo-3.1-fast-generate-preview` | 중간 | 빠른 생성 |
| Veo 3.1 Lite | `veo-3.1-lite-generate-preview` | 저렴 (Fast의 50%) | 대량 생성 |

## 기본 사용법 (Python)
```python
from google import genai
from google.genai import types
import time

client = genai.Client()

# 텍스트 → 영상
operation = client.models.generate_videos(
    model="veo-3.1-generate-preview",
    prompt="A cute baby sleeping peacefully in a cozy nursery, soft lighting, vertical video",
    config=types.GenerateVideosConfig(
        aspect_ratio="9:16",  # 세로 (쇼츠)
        number_of_videos=1,
    )
)

# 완료 대기
while not operation.done:
    time.sleep(10)
    operation = client.operations.get(operation)

# 저장
video = operation.response.generated_videos[0]
with open("scene.mp4", "wb") as f:
    f.write(video.video.video_bytes)
```

## 이미지 → 영상 (Nano Banana 2 연계)
```python
# Step 1: 이미지 생성
image_response = client.models.generate_content(
    model="gemini-3.1-flash-image-preview",
    contents="A cute baby sleeping in a nursery, vertical format",
    config={"response_modalities": ["IMAGE"]}
)

# Step 2: 이미지 → 영상
operation = client.models.generate_videos(
    model="veo-3.1-generate-preview",
    prompt="Smooth camera pan across the nursery scene",
    image=image_response.parts[0].as_image(),
)
```

## 주요 기능
- **9:16 세로 영상**: 쇼츠/릴스 최적화
- **8초 클립**: 기본 생성 길이
- **Scene Extension**: 이전 영상의 마지막 1초를 이어서 연장 가능
- **Reference Images**: 최대 3개 참조 이미지로 스타일/캐릭터 일관성 유지
- **네이티브 오디오**: Veo 3.1에서 효과음/대화 자동 생성
- **SynthID**: AI 생성 워터마크 자동 포함

## 해상도 옵션
- 720p (기본)
- 1080p
- 4K (Veo 3.1 only)

## 가격
- Veo 3.1 Lite가 가장 경제적 (Fast의 ~50%)
- 유료 Gemini API 티어 필요
