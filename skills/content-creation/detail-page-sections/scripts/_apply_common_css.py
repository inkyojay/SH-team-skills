#!/usr/bin/env python3
"""
Update all detail page HTML files to use _common.css instead of inline <style> blocks.
- Removes <style>...</style> block
- Adds <link rel="stylesheet" href="_common.css"> after Google Fonts link
- Keeps everything else intact (inline style="" attributes, scripts, etc.)
"""
import re
from pathlib import Path

CURRENT_DIR = Path(__file__).parent
SKIP_PATTERNS = ['silky_bamboo', 'capture.py', '_build', '_common', '_apply']
CSS_LINK = '<link rel="stylesheet" href="_common.css">'
GOOGLE_FONTS_URL = 'https://fonts.googleapis.com/css2?family=Cormorant+Garamond'

def should_skip(name):
    return any(p in name for p in SKIP_PATTERNS)

def process_file(filepath):
    html = filepath.read_text('utf-8')

    # Check if already using _common.css
    if '_common.css' in html:
        return False

    # Remove <style>...</style> block
    new_html = re.sub(r'\n?<style>.*?</style>\n?', '\n', html, flags=re.DOTALL)

    # Add CSS link after Google Fonts link (or before </head> if no Fonts link)
    if GOOGLE_FONTS_URL in new_html:
        new_html = re.sub(
            r'(rel="stylesheet">)',
            f'rel="stylesheet">\n{CSS_LINK}',
            new_html,
            count=1
        )
    else:
        new_html = new_html.replace('</head>', f'{CSS_LINK}\n</head>')

    # Also add Google Fonts link if missing
    google_fonts = '<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,500;0,600;1,300;1,400&family=Noto+Sans+KR:wght@300;400;500;700&family=DM+Sans:ital,wght@0,300;0,400;0,500;1,300&display=swap" rel="stylesheet">'
    if 'fonts.googleapis.com' not in new_html:
        new_html = new_html.replace(CSS_LINK, f'{google_fonts}\n{CSS_LINK}')

    # Remove Figma capture script if present (development-only)
    new_html = re.sub(r'\n?<script src="https://mcp\.figma\.com[^"]*"[^>]*></script>\n?', '\n', new_html)

    filepath.write_text(new_html, 'utf-8')
    return True

def main():
    files = sorted(CURRENT_DIR.glob('*.html'))
    updated = 0
    skipped = 0

    for f in files:
        if should_skip(f.name):
            skipped += 1
            continue

        if process_file(f):
            print(f'  Updated: {f.name}')
            updated += 1
        else:
            print(f'  Already OK: {f.name}')

    print(f'\nDone: {updated} updated, {skipped} skipped')

if __name__ == '__main__':
    main()
