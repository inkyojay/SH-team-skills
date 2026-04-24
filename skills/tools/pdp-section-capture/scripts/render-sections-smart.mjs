// Smart section splitter — uses HTML comments as section labels.
//
// Rules:
//   1. Walk direct children of <main container>
//   2. Use preceding HTML comment as label (e.g., <!-- HERO -->)
//      Skip placeholder comments like "Content", "Styles"
//   3. SKIP elements whose class is exactly "divider" (decorative)
//   4. MERGE small standalone elements (class "eq", height < 400px) into PREVIOUS section
//   5. Filename: NN_<sanitized-label>.<ext>
//
// SUPERSAMPLING: render at superScale × cssWidth, then downsample to (outScale × cssWidth)
// using lanczos3. This gives noticeably crisper text than rendering at outScale directly,
// because Chrome's subpixel AA + photographic detail are averaged into clean grayscale.
//
// Usage:
//   node render-sections-smart.mjs <html> <outDir>
//        [container=.pdp-absolute] [cssWidth=600] [outScale=2] [format=png] [quality=92] [superScale=3]
//   outScale=2 + superScale=3 → render at 1800px, downsample to 1200px (recommended)

import puppeteer from 'puppeteer';
import sharp from 'sharp';
import path from 'path';
import fs from 'fs';
import os from 'os';

const [, , htmlPath, outDir, containerArg, widthArg, scaleArg, fmtArg, qArg, superArg] = process.argv;
const containerSel = containerArg || '.pdp-absolute';
const cssWidth = parseInt(widthArg || '600', 10);
const outScale = parseFloat(scaleArg || '2');           // final output scale (e.g. 2 → 1200px)
const superScale = parseFloat(superArg || '3');         // render scale (e.g. 3 → 1800px native)
const format = (fmtArg || 'png').toLowerCase();
const quality = parseInt(qArg || '92', 10);
// We'll render at superScale, then downsample each crop to outScale via lanczos3
const deviceScaleFactor = superScale;
const finalPixelWidth = Math.round(cssWidth * outScale);

if (!fs.existsSync(outDir)) fs.mkdirSync(outDir, { recursive: true });

const SKIP_LABELS = new Set(['CONTENT', 'STYLES', '']);

// Utility / modifier classes that are not meaningful section identifiers on their own.
// When no HTML comment label is available, we'll skip these when picking a class-based fallback.
const SKIP_CLASSES = new Set([
  'v', 'on', 'divider', 'soft', 'tight', 'inset', 'rev', 'first', 'last', 'full',
  'center', 'left', 'right', 'tx-c', 'tx-l', 'tx-r', 'hl',
]);

// SundayHug PDP semantic class prefixes. If present in the element's class list,
// these are preferred over a generic first class token. Matches the KNOWN list
// used by the Python variant of this skill.
const KNOWN_SECTION_CLASSES = [
  'hero', 'badge-bar', 'trust-bar', 'sec', 'feat', 'fi', 'cmp', 'eq', 'notice',
  'rv-section', 'faq-list', 'final-cta', 'product-info', 'wash-sec', 'mid-cta',
];

const browser = await puppeteer.launch({
  headless: 'new',
  args: ['--no-sandbox', '--allow-file-access-from-files'],
  defaultViewport: { width: cssWidth, height: 800, deviceScaleFactor },
});
const page = await browser.newPage();
// Neuter IntersectionObserver BEFORE any page script runs.
// The detail page's inline script does `io.observe(el)` to add `.on` later.
// Replace with a no-timing version that fires the callback immediately, so every
// `.v` element is `.on` from the very first paint. No timing race possible.
await page.evaluateOnNewDocument(() => {
  // eslint-disable-next-line no-global-assign
  window.IntersectionObserver = class {
    constructor(cb) { this.cb = cb; }
    observe(el) {
      try { this.cb([{ target: el, isIntersecting: true, intersectionRatio: 1, time: 0, boundingClientRect: el.getBoundingClientRect(), intersectionRect: el.getBoundingClientRect(), rootBounds: null }], this); } catch (e) {}
    }
    unobserve() {}
    disconnect() {}
    takeRecords() { return []; }
  };
});
await page.goto('file://' + htmlPath, { waitUntil: 'networkidle0', timeout: 60000 });

// Inject crisp-text CSS + zero out browser-default body/html margins (8px each side) so
// the .pdp-absolute (max-width:600) sits flush against the viewport edge.
// Also force-reveal .v elements (belt & suspenders alongside the IO neuter above).
await page.addStyleTag({ content: `
  html, body { margin: 0 !important; padding: 0 !important; background: #fff; }
  .pdp-absolute .v,
  .pdp-absolute .v.on { opacity: 1 !important; transform: none !important; filter: none !important; }
  /* Note: do NOT force -webkit-font-smoothing here — let Chrome use its native subpixel AA
     at the supersampled resolution; the lanczos3 downsample will average out color fringing
     into clean grayscale and produce sharper edges than direct grayscale AA at low res. */
  *, *::before, *::after {
    text-rendering: geometricPrecision !important;
    animation: none !important;
    transition: none !important;
  }
` });

// Wait for fonts (including @import'd Google Fonts inside stylesheets)
await page.evaluate(async () => {
  if (document.fonts && document.fonts.ready) await document.fonts.ready;
});
// Explicit pre-load of expected font families via FontFaceSet.load()
await page.evaluate(async () => {
  const faces = [
    '300 1em "Noto Sans KR"','400 1em "Noto Sans KR"','500 1em "Noto Sans KR"','700 1em "Noto Sans KR"',
    '300 1em "DM Sans"','400 1em "DM Sans"','500 1em "DM Sans"',
    '300 1em "Cormorant Garamond"','400 1em "Cormorant Garamond"','500 1em "Cormorant Garamond"','600 1em "Cormorant Garamond"',
  ];
  await Promise.all(faces.map(f => document.fonts.load(f).catch(()=>null)));
  await document.fonts.ready;
});
await page.evaluate(() => {
  document.querySelectorAll('.v').forEach(el => el.classList.add('on'));
  document.querySelectorAll('[data-aos], .reveal, .fade-in, .scroll-reveal').forEach(el => {
    el.classList.add('aos-animate', 'on', 'visible', 'in-view');
  });
});
await page.evaluate(async () => {
  const distance = 600, delay = 80;
  const total = document.documentElement.scrollHeight;
  for (let y = 0; y < total; y += distance) { window.scrollTo(0, y); await new Promise(r => setTimeout(r, delay)); }
  window.scrollTo(0, 0); await new Promise(r => setTimeout(r, 300));
});
await page.evaluate(async () => {
  const imgs = Array.from(document.images);
  await Promise.all(imgs.map(img => img.complete ? null : new Promise(r => { img.onload = img.onerror = r; })));
});
await new Promise(r => setTimeout(r, 1500));

// IMPORTANT: lock the viewport to the full document height NOW, so that when we take
// per-section clipped screenshots later there is no internal viewport resize / reflow
// that could shift section coordinates between measurement and capture.
const docHeight = await page.evaluate(() => document.documentElement.scrollHeight);
await page.setViewport({ width: cssWidth, height: docHeight, deviceScaleFactor });
await page.evaluate(() => window.scrollTo(0, 0));
await new Promise(r => setTimeout(r, 500));
// Re-wait for any images that may have triggered loading after the viewport resize
await page.evaluate(async () => {
  const imgs = Array.from(document.images);
  await Promise.all(imgs.map(img => img.complete ? null : new Promise(r => { img.onload = img.onerror = r; })));
});
await new Promise(r => setTimeout(r, 500));

// Walk children, tag each with a data-section-idx so we can fetch their live bbox later.
const raw = await page.evaluate((containerSel) => {
  const root = document.querySelector(containerSel) || document.body;
  const out = [];
  let i = 0;
  for (const child of root.children) {
    const r = child.getBoundingClientRect();
    if (r.height <= 0) continue;

    // tag the element so we can re-query it later by stable selector
    child.setAttribute('data-section-idx', String(i));

    // find preceding comment label by walking previousSibling nodes
    let label = '';
    let n = child.previousSibling;
    while (n) {
      if (n.nodeType === 8 /* COMMENT */) {
        const txt = n.nodeValue.trim();
        if (txt) { label = txt; break; }
      } else if (n.nodeType === 1 /* ELEMENT */) {
        break;
      }
      n = n.previousSibling;
    }
    out.push({
      idx: i,
      label,
      cssTop: window.scrollY + r.top,
      cssHeight: r.height,
      cls: child.className || '',
      tag: child.tagName.toLowerCase(),
    });
    i++;
  }
  return out;
}, containerSel);

// We don't need a fullpage temp PNG anymore — each section will be captured live.
const pixelWidth = Math.round(cssWidth * deviceScaleFactor);
const pixelHeight = Math.round(docHeight * deviceScaleFactor);

// Apply rules: skip dividers, merge eq into previous section
const groups = []; // { label, top, bottom, members:[{cls, label, ...}] }
for (const r of raw) {
  const isDivider = r.cls.split(/\s+/).includes('divider');
  if (isDivider) continue; // skip decorative

  const isEq = r.cls.split(/\s+/).includes('eq');
  const isSmall = r.cssHeight < 400;
  const labelClean = (r.label || '').toUpperCase().trim();
  const isSkipLabel = SKIP_LABELS.has(labelClean);

  // candidate to merge into previous: small eq, OR no useful label and tiny
  const shouldMerge = (isEq && isSmall) && groups.length > 0;

  if (shouldMerge) {
    const last = groups[groups.length - 1];
    last.bottom = Math.max(last.bottom, r.cssTop + r.cssHeight);
    last.members.push(r);
    continue;
  }

  // skip elements with no label and no class (shouldn't happen but safe)
  if (!r.label && !r.cls) continue;

  // pick label — preference order:
  //   1. HTML comment label (if useful)
  //   2. First KNOWN_SECTION_CLASSES hit in element's class list
  //   3. First non-utility class (not in SKIP_CLASSES)
  //   4. Raw first class, or tagName as last resort
  let label;
  const classes = r.cls.split(/\s+/).filter(Boolean);
  if (r.label && !isSkipLabel) {
    label = r.label;
  } else {
    const known = KNOWN_SECTION_CLASSES.find(k => classes.includes(k));
    const meaningful = classes.find(c => !SKIP_CLASSES.has(c));
    label = known || meaningful || classes[0] || r.tag;
  }

  groups.push({
    label,
    top: r.cssTop,
    bottom: r.cssTop + r.cssHeight,
    members: [r],
  });
}

// Render each group as a LIVE clipped screenshot (no fullpage temp PNG).
// For each group, fetch the current bounding box of all its members RIGHT BEFORE the
// screenshot — this guarantees coords match the actual DOM state at capture time,
// so a section can never be cut mid-content due to layout shift between measure & capture.
const stem = path.basename(htmlPath, '.html');
const written = [];
let n = 0;
for (const g of groups) {
  n++;
  const safeLabel = g.label
    .replace(/[\/\\:*?"<>|]/g, '')
    .replace(/\s*:\s*/g, '-')
    .replace(/\s+/g, '-')
    .replace(/-+/g, '-')
    .replace(/^-|-$/g, '')
    .slice(0, 60);

  // Live re-measure of all member elements (single bounding box covering the union)
  const memberIdxs = g.members.map(m => m.idx);
  const live = await page.evaluate((idxs, containerSel) => {
    const root = document.querySelector(containerSel) || document.body;
    let top = Infinity, bottom = -Infinity;
    for (const i of idxs) {
      const el = root.querySelector(`:scope > [data-section-idx="${i}"]`);
      if (!el) continue;
      const r = el.getBoundingClientRect();
      const t = window.scrollY + r.top;
      const b = t + r.height;
      if (t < top) top = t;
      if (b > bottom) bottom = b;
    }
    return { top, bottom };
  }, memberIdxs, containerSel);

  if (!isFinite(live.top) || !isFinite(live.bottom) || live.bottom <= live.top) continue;

  // Round CSS coords; use clip in CSS pixels (Puppeteer multiplies by deviceScaleFactor itself)
  const cssY = Math.max(0, Math.floor(live.top));
  const cssH = Math.ceil(live.bottom - live.top);

  const file = path.join(outDir, `${String(n).padStart(2, '0')}_${safeLabel || 'section'}.${format}`);

  // Live clipped screenshot — captures EXACTLY this section's current pixels
  const buffer = await page.screenshot({
    clip: { x: 0, y: cssY, width: cssWidth, height: cssH },
    type: 'png',
    omitBackground: false,
  });

  // Buffer is at supersampled resolution (cssWidth*deviceScaleFactor wide).
  // Downsample to finalPixelWidth via lanczos3, preserving aspect ratio explicitly.
  let pl = sharp(buffer);
  if (finalPixelWidth !== pixelWidth) {
    const targetH = Math.round(cssH * outScale);
    pl = pl.resize({ width: finalPixelWidth, height: targetH, kernel: 'lanczos3', fit: 'fill' });
  }
  if (format === 'png') pl = pl.png({ compressionLevel: 9 });
  else if (format === 'webp') pl = pl.webp({ quality });
  else pl = pl.jpeg({ quality, mozjpeg: true });
  await pl.toFile(file);

  written.push({
    file: path.basename(file),
    size_kb: Math.round(fs.statSync(file).size / 1024),
    cssY, cssH,
    members: g.members.length,
    classes: g.members.map(m => m.cls).slice(0, 3),
  });
}

await browser.close();
console.log(JSON.stringify({
  containerSel, cssWidth, scale: deviceScaleFactor, format, quality,
  pixelWidth, pixelHeight,
  rawChildren: raw.length,
  groupsAfterMerge: groups.length,
  filesWritten: written.length,
  files: written,
}, null, 2));
