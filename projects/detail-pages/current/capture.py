#!/usr/bin/env python3
"""섹션별 캡처 - full page 이미지를 PIL로 잘라내기"""
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image

HTML_FILE = sys.argv[1] if len(sys.argv) > 1 else "sleepsack_silky_bamboo.html"
WIDTH = 600
SCALE = 2  # 고해상도 (2x = 1200px 출력)
html_path = Path(HTML_FILE).resolve()
out_dir = html_path.parent / f"{html_path.stem}_sections"
out_dir.mkdir(exist_ok=True)

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(
        viewport={"width": WIDTH, "height": 800},
        device_scale_factor=SCALE
    )
    page.goto(f"file://{html_path}", wait_until="networkidle")
    page.wait_for_timeout(1000)

    # 모든 애니메이션/opacity 강제 해제
    page.add_style_tag(content="""
        *, *::before, *::after {
            animation: none !important;
            transition: none !important;
        }
        .v { opacity: 1 !important; transform: none !important; }
    """)
    page.wait_for_timeout(500)

    # 전체 페이지 캡처
    full_path = out_dir / "00_full_page.png"
    page.screenshot(path=str(full_path), full_page=True)
    print("✅ 00_full_page.png")

    # body 직속 자식 요소들의 위치 정보 수집
    sections = page.evaluate("""() => {
        const children = document.body.children;
        const results = [];
        for (let i = 0; i < children.length; i++) {
            const el = children[i];
            if (el.tagName === 'SCRIPT' || el.tagName === 'STYLE') continue;
            const rect = el.getBoundingClientRect();
            const top = Math.round(rect.top + window.scrollY);
            const height = Math.round(rect.height);
            if (height < 5) continue;

            let name = '';
            let prev = el.previousSibling;
            while (prev) {
                if (prev.nodeType === 8) {
                    const text = prev.textContent.trim();
                    if (text.match(/^[A-Z]/)) { name = text; break; }
                }
                prev = prev.previousSibling;
            }
            if (!name) name = el.className || el.tagName;
            results.push({ name, top, height });
        }
        return results;
    }""")

    browser.close()

# PIL로 전체 이미지를 잘라내기
full_img = Image.open(full_path)
img_w, img_h = full_img.size
print(f"\n전체 이미지: {img_w}x{img_h}px")
print(f"섹션 수: {len(sections)}\n")

for i, s in enumerate(sections):
    name = s['name'].replace(' ', '_').replace(':', '').replace('--', '').replace('&', '')
    name = ''.join(c for c in name if c.isascii() and (c.isalnum() or c == '_'))
    name = name.strip('_').lower() or f"section_{i}"
    fname = f"{i+1:02d}_{name}.png"

    top = int(s['top'] * SCALE)
    height = int(s['height'] * SCALE)
    bottom = min(top + height, img_h)

    if height < 10:
        continue

    cropped = full_img.crop((0, top, img_w, bottom))
    cropped.save(out_dir / fname)
    print(f"✅ {fname} ({s['height']}px)")

print(f"\n📁 저장 폴더: {out_dir}")
print(f"📊 총 {len(sections) + 1}개 이미지")
