#!/usr/bin/env python3
"""
Extract CSS from all detail page HTML files, merge into a single common CSS.
Uses 1.45x enlarged font sizes. Prefer rules from scaled files;
scale old-file-only rules by 1.45x.
"""
import re
from pathlib import Path
from collections import OrderedDict

CURRENT_DIR = Path(__file__).parent

SKIP_PATTERNS = ['silky_bamboo', 'capture.py', '_build', '_common']

# Files with confirmed 1.45x font sizes (hero h1 = 38px)
SCALED_FILES = {
    'body-bamboo.html', 'body-mesh.html',
    'abc-cover.html', 'abc-mosquito-net.html', 'abc-organizer.html',
    'sleepsack_all.html', 'swaddle-sb.html', 'swaddle-set.html', 'whitenoise.html',
}

# Known 1.45x font-size values (don't re-scale these)
KNOWN_145X = {16,17,14,19,20,22,25,26,29,32,35,38,46,52}

def should_skip(name):
    return any(p in name for p in SKIP_PATTERNS)

def extract_style(html):
    m = re.search(r'<style>(.*?)</style>', html, re.DOTALL)
    return m.group(1) if m else ''

def strip_comments(css):
    return re.sub(r'/\*.*?\*/', '', css, flags=re.DOTALL)

def extract_root(css):
    m = re.search(r':root\s*\{([^}]+)\}', css)
    return m.group(0) if m else ''

def extract_keyframes(css):
    kfs = OrderedDict()
    for m in re.finditer(r'@keyframes\s+(\w+)\s*\{([^}]*\{[^}]*\}[^}]*)\}', css):
        kfs[m.group(1)] = m.group(0)
    return kfs

def extract_rules(css):
    """Extract CSS rules, returning OrderedDict of selector -> body."""
    # Remove :root and @keyframes first
    clean = re.sub(r':root\s*\{[^}]+\}', '', css)
    clean = re.sub(r'@keyframes\s+\w+\s*\{[^}]*\{[^}]*\}[^}]*\}', '', clean)

    rules = OrderedDict()
    for m in re.finditer(r'([^{}]+?)\{([^}]+)\}', clean):
        sel = m.group(1).strip()
        body = m.group(2).strip()
        if sel and body and not sel.startswith('@'):
            # Normalize whitespace
            sel = ' '.join(sel.split())
            rules[sel] = body
    return rules

def scale_font_sizes(body):
    """Scale font-size values by 1.45x."""
    def do_scale(m):
        val = float(m.group(1))
        scaled = round(val * 1.45)
        return f'font-size:{scaled}px'
    return re.sub(r'font-size:(\d+(?:\.\d+)?)px', do_scale, body)

def fix_weight(body):
    return body.replace('font-weight:300', 'font-weight:400')

def main():
    # Collect from all files
    root_block = ''
    all_keyframes = OrderedDict()
    # selector -> (body, is_from_scaled_file)
    all_rules = OrderedDict()

    files = sorted(CURRENT_DIR.glob('*.html'))
    for f in files:
        if should_skip(f.name):
            continue
        html = f.read_text('utf-8')
        css = strip_comments(extract_style(html))
        if not css:
            continue

        is_scaled = f.name in SCALED_FILES

        # Root vars - prefer from scaled file
        r = extract_root(css)
        if r and (not root_block or is_scaled):
            root_block = r

        # Keyframes
        for name, kf in extract_keyframes(css).items():
            if name not in all_keyframes:
                all_keyframes[name] = kf

        # Rules
        for sel, body in extract_rules(css).items():
            if sel not in all_rules:
                all_rules[sel] = (body, is_scaled)
            elif is_scaled and not all_rules[sel][1]:
                all_rules[sel] = (body, True)

    # Scale rules from non-scaled files
    final_rules = OrderedDict()
    for sel, (body, is_scaled) in all_rules.items():
        if not is_scaled:
            body = scale_font_sizes(body)
            body = fix_weight(body)
        final_rules[sel] = body

    # Also scale old sizes in "scaled" files that were missed
    # (e.g. compare-card-tag:10px in sleepsack_all.html)
    for sel, body in final_rules.items():
        # Find font-size values that are clearly old (small)
        def maybe_scale(m):
            val = int(m.group(1))
            # Values <= 13px are likely old unscaled sizes
            if val <= 13 and val not in (12,):  # 12px for icon font is OK
                return f'font-size:{round(val * 1.45)}px'
            return m.group(0)

        # Only scale specific selectors known to have mixed sizes
        if any(p in sel for p in ['.compare-card', '.sub-3col', '.sg-', '.color-var-name',
                                   '.detail-item-label', '.rv-', '.sub-pt-',
                                   '.care-', '.ship-', '.other-', '.mat-tbl',
                                   '.event-', '.fabric-', '.alert', '.comp-',
                                   '.link-btn', '.qty']):
            final_rules[sel] = re.sub(r'font-size:(\d+)px', maybe_scale, body)

    # Define section order for output
    sections = [
        ('Reset', ['*', 'html', 'body', 'img']),
        ('Hero', '.hero'),
        ('Trust Bar', '.trust-bar'),
        ('Sections', '.sec'),
        ('Typography', ['.tx-center', '.tx-c', '.hl', '.hl-sage', '.thin-line']),
        ('Images', ['.fb-img', '.sec-img', '.fi']),
        ('Block Quote', '.bq'),
        ('Features', '.feat'),
        ('Sub-Points', '.sub-pt'),
        ('2-Column Sub', '.sub-2col'),
        ('3-Column Sub', '.sub-3col'),
        ('3-Column Trust', '.trust-3'),
        ('Color Variation', '.color-var'),
        ('Detail Grid', ['.detail-grid', '.detail-item']),
        ('Size Table', '.sz-tbl'),
        ('Material Table', '.mat-tbl'),
        ('Info Table', '.info-tbl'),
        ('Reviews', '.rv'),
        ('Note Card', '.note-'),
        ('Step List', '.step-'),
        ('Callout', '.callout'),
        ('FAQ', '.faq-'),
        ('Compare Cards', '.compare'),
        ('Care Instructions', '.care-'),
        ('Shipping', '.ship-'),
        ('Other Products', '.other'),
        ('Link Button', '.link-btn'),
        ('Events', '.event'),
        ('Fabric Comparison', '.fabric-'),
        ('Sleep Guide', '.sg-'),
        ('Alert Box', '.alert-'),
        ('Competition Grid', '.comp-'),
        ('Quantity', '.qty'),
        ('Final CTA', '.final-cta'),
        ('Close & Footer', ['.close', '.footer']),
    ]

    out = []
    out.append('/* Sunday Hug - Detail Page Common Styles (1.45x Font Size)')
    out.append('   Link: <link rel="stylesheet" href="_common.css"> */')
    out.append('')
    out.append(root_block)
    out.append('')

    # Animations
    out.append('/* === Reset === */')
    for sel in ['*', 'html', 'body', 'img']:
        if sel in final_rules:
            out.append(f'{sel}{{{final_rules.pop(sel)}}}')
    out.append('')

    out.append('/* === Animations === */')
    for kf in all_keyframes.values():
        out.append(kf)
    for sel in ['.v', '.v.on']:
        if sel in final_rules:
            out.append(f'{sel}{{{final_rules.pop(sel)}}}')
    out.append('')

    used = set()

    for section_name, pattern in sections:
        if section_name == 'Reset':
            continue  # Already handled

        matches = []
        if isinstance(pattern, list):
            prefixes = pattern
        else:
            prefixes = [pattern]

        for sel in list(final_rules.keys()):
            if sel in used:
                continue
            for pfx in prefixes:
                if sel == pfx or sel.startswith(pfx) or (f' {pfx}' in sel) or (f'+{pfx}' in sel):
                    matches.append((sel, final_rules[sel]))
                    used.add(sel)
                    break

        if matches:
            out.append(f'/* === {section_name} === */')
            for sel, body in matches:
                out.append(f'{sel}{{{body}}}')
            out.append('')

    # Remaining
    remaining = [(s, final_rules[s]) for s in final_rules if s not in used and s not in ('*', 'html', 'body', 'img', '.v', '.v.on')]
    if remaining:
        out.append('/* === Other === */')
        for sel, body in remaining:
            out.append(f'{sel}{{{body}}}')
        out.append('')

    output_path = CURRENT_DIR / '_common.css'
    output_path.write_text('\n'.join(out), encoding='utf-8')

    total = sum(1 for s in final_rules) + 4  # +4 for *, html, body, img
    print(f'Written: {output_path}')
    print(f'Rules: {total}, Keyframes: {len(all_keyframes)}')

if __name__ == '__main__':
    main()
