#!/bin/bash
# 미디어 소스 심링크 생성
# 실행: bash setup.sh

MEDIA_SOURCE="/Users/inkyo/Downloads/슬리핑백"
SYMLINK_TARGET="public/media"

if [ -L "$SYMLINK_TARGET" ]; then
  echo "심링크가 이미 존재합니다: $SYMLINK_TARGET"
elif [ -d "$MEDIA_SOURCE" ]; then
  ln -s "$MEDIA_SOURCE" "$SYMLINK_TARGET"
  echo "심링크 생성 완료: $SYMLINK_TARGET -> $MEDIA_SOURCE"
else
  echo "미디어 소스 폴더를 찾을 수 없습니다: $MEDIA_SOURCE"
  exit 1
fi

echo ""
echo "다음 단계:"
echo "  npm install"
echo "  npm run dev"
