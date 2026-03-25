---
name: hwpx
description: "HWPX(아래아 한글) 문서 변환 도구. DOCX, Markdown, HTML 파일을 한글 문서(.hwpx)로 변환합니다. 사용자가 문서를 hwpx로 변환하거나 아래아 한글 형식으로 저장할 때 사용합니다."
---

# HWPX Document Converter

## Overview

pypandoc-hwpx를 사용하여 다양한 문서 형식을 아래아 한글(.hwpx) 문서로 변환합니다.

## When to Use

사용자가 다음과 같은 요청을 할 때 이 스킬을 사용합니다:
- "문서를 hwpx로 변환해줘"
- "docx를 한글 파일로 바꿔줘"
- "마크다운을 hwpx로 만들어줘"
- "html을 아래아 한글로 변환"
- "한글 문서로 저장해줘"

## Basic Usage

```bash
pypandoc-hwpx <input_file> -o <output_file.hwpx>
```

### Examples

```bash
# DOCX -> HWPX
pypandoc-hwpx document.docx -o document.hwpx

# Markdown -> HWPX
pypandoc-hwpx readme.md -o readme.hwpx

# HTML -> HWPX
pypandoc-hwpx page.html -o page.hwpx

# JSON AST -> HWPX (Pandoc JSON 형식)
pypandoc-hwpx data.json -o data.hwpx
```

## Advanced Usage

### 커스텀 스타일 템플릿 사용

기존 HWPX 파일의 스타일(글꼴, 문단, 페이지 설정)을 복제하여 사용할 수 있습니다:

```bash
pypandoc-hwpx document.docx --reference-doc=custom.hwpx -o output.hwpx
```

### 디버깅용 출력

```bash
# HTML로 변환 (확인용)
pypandoc-hwpx document.docx -o document.html

# JSON AST로 변환 (디버깅용)
pypandoc-hwpx document.docx -o document.json
```

## Supported Input Formats

| 입력 형식 | 확장자 | 설명 |
|----------|--------|------|
| Microsoft Word | .docx | 워드 문서 |
| Markdown | .md | 마크다운 |
| HTML | .html, .htm | 웹 페이지 |
| Pandoc JSON | .json | Pandoc AST 형식 |

## Supported Features

- 제목 (H1~H6)
- 본문 텍스트
- 굵게, 기울임, 밑줄, 위첨자, 아래첨자
- 번호 목록, 글머리 기호 목록
- 표 (셀 병합 포함)
- 이미지
- 하이퍼링크
- 각주
- 코드 블록

## Options

| 옵션 | 설명 |
|------|------|
| `-o, --output` | 출력 파일 경로 (필수) |
| `--reference-doc` | 스타일 참조용 HWPX 템플릿 (선택) |

## Notes

- 출력 확장자에 따라 변환 형식이 결정됩니다
- 기본 템플릿(`blank.hwpx`)이 패키지에 내장되어 있습니다
- Pandoc이 시스템에 설치되어 있어야 합니다

## Dependencies

- Python 3.6+
- Pandoc (시스템 설치)
- pypandoc
- Pillow
