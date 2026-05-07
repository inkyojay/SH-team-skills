#!/usr/bin/env node

import fs from "node:fs/promises";
import os from "node:os";
import path from "node:path";
import { createRequire } from "node:module";
import { pathToFileURL } from "node:url";

const require = createRequire(import.meta.url);

const defaults = {
  mode: "all",
  mobileWidth: 430,
  viewportHeight: 2200,
  scale: 3,
  quality: 92,
  thumbSize: 1080,
  sectionSelector:
    "[data-export-section], main section, body > section, .bl-hero, .bl-benefit, .bl-section, .bl-product, .bl-notice, .bl-final-cta",
  strict: false,
};

function parseArgs(argv) {
  const args = { ...defaults };
  for (let i = 0; i < argv.length; i += 1) {
    const raw = argv[i];
    if (!raw.startsWith("--")) continue;

    const [keyRaw, inlineValue] = raw.slice(2).split("=", 2);
    const key = keyRaw.replace(/-([a-z])/g, (_, c) => c.toUpperCase());
    const next = argv[i + 1];
    const value =
      inlineValue !== undefined
        ? inlineValue
        : next && !next.startsWith("--")
          ? (i += 1, next)
          : true;

    args[key] = value;
  }

  for (const key of ["mobileWidth", "viewportHeight", "scale", "quality", "thumbSize"]) {
    args[key] = Number(args[key]);
  }
  args.strict = args.strict === true || args.strict === "true" || args.strict === "1";
  return args;
}

function expandHome(input) {
  if (!input) return input;
  return input.startsWith("~/") ? path.join(os.homedir(), input.slice(2)) : input;
}

function slugify(input) {
  return String(input || "event-page")
    .normalize("NFKD")
    .replace(/[^\p{L}\p{N}]+/gu, "-")
    .replace(/^-+|-+$/g, "")
    .slice(0, 80)
    .toLowerCase() || "event-page";
}

function toPageUrl(input) {
  if (/^https?:\/\//.test(input) || input.startsWith("file://")) return input;
  return pathToFileURL(path.resolve(expandHome(input))).href;
}

function defaultOutDir(htmlPathOrUrl) {
  const base = htmlPathOrUrl.startsWith("file://")
    ? path.basename(new URL(htmlPathOrUrl).pathname, path.extname(new URL(htmlPathOrUrl).pathname))
    : /^https?:\/\//.test(htmlPathOrUrl)
      ? new URL(htmlPathOrUrl).hostname
      : path.basename(expandHome(htmlPathOrUrl), path.extname(expandHome(htmlPathOrUrl)));

  return path.join(
    os.homedir(),
    "Desktop",
    "team-skills",
    "상세페이지",
    "event-campaign",
    slugify(base),
  );
}

function fileNameFor(index, label) {
  return `${String(index).padStart(2, "0")}-${slugify(label || "section")}.jpg`;
}

async function loadPlaywright() {
  try {
    return require("playwright");
  } catch (error) {
    console.error("Playwright를 찾을 수 없습니다.");
    console.error("먼저 실행하세요:");
    console.error("  cd /Users/inkyo/Projects/team-skills/skills/promotion/event-page-campaign/scripts");
    console.error("  npm install");
    throw error;
  }
}

async function ensureDir(dir) {
  await fs.mkdir(dir, { recursive: true });
}

async function waitForStablePage(page) {
  await page.addStyleTag({
    content: `
      *, *::before, *::after {
        animation-duration: 0s !important;
        animation-delay: 0s !important;
        transition-duration: 0s !important;
        scroll-behavior: auto !important;
      }
      html, body { margin-left: 0 !important; margin-right: 0 !important; }
    `,
  }).catch(() => {});

  await page.evaluate(async () => {
    if (document.fonts?.ready) await document.fonts.ready;
    const images = Array.from(document.images);
    await Promise.all(images.map((img) => {
      if (img.complete) return Promise.resolve();
      return new Promise((resolve) => {
        img.addEventListener("load", resolve, { once: true });
        img.addEventListener("error", resolve, { once: true });
      });
    }));
  });

  await page.waitForTimeout(350);
}

async function openReadyPage(context, url) {
  const page = await context.newPage();
  await page.goto(url, { waitUntil: "load" });
  await page.waitForLoadState("networkidle", { timeout: 5000 }).catch(() => {});
  await waitForStablePage(page);
  return page;
}

async function inspectPage(page) {
  return page.evaluate(() => {
    const viewportWidth = document.documentElement.clientWidth;
    const scrollWidth = Math.max(document.documentElement.scrollWidth, document.body?.scrollWidth || 0);
    const scrollHeight = Math.max(document.documentElement.scrollHeight, document.body?.scrollHeight || 0);
    const brokenImages = Array.from(document.images)
      .filter((img) => !img.complete || img.naturalWidth === 0)
      .map((img) => img.currentSrc || img.src || img.getAttribute("src") || "")
      .slice(0, 20);

    const overflowing = Array.from(document.body.querySelectorAll("*"))
      .map((el) => {
        const rect = el.getBoundingClientRect();
        return {
          tag: el.tagName.toLowerCase(),
          cls: String(el.className || "").slice(0, 90),
          id: el.id || "",
          left: Math.round(rect.left),
          right: Math.round(rect.right),
          width: Math.round(rect.width),
        };
      })
      .filter((item) => item.width > 0 && (item.right > viewportWidth + 2 || item.left < -2))
      .slice(0, 20);

    const textOverflow = Array.from(document.body.querySelectorAll("p, li, h1, h2, h3, h4, span, a, button, strong"))
      .filter((el) => el.scrollWidth > el.clientWidth + 2 && el.clientWidth > 0)
      .map((el) => ({
        tag: el.tagName.toLowerCase(),
        cls: String(el.className || "").slice(0, 90),
        text: (el.textContent || "").trim().replace(/\s+/g, " ").slice(0, 120),
      }))
      .slice(0, 20);

    return {
      title: document.title,
      viewportWidth,
      scrollWidth,
      scrollHeight,
      horizontalOverflow: scrollWidth > viewportWidth + 2 || overflowing.length > 0,
      brokenImages,
      overflowing,
      textOverflow,
    };
  });
}

async function captureMobile({ browser, url, outDir, slug, args }) {
  const context = await browser.newContext({
    viewport: { width: args.mobileWidth, height: args.viewportHeight },
    deviceScaleFactor: args.scale,
    isMobile: true,
  });
  const page = await openReadyPage(context, url);
  const report = await inspectPage(page);

  const mobileDir = path.join(outDir, "mobile");
  await ensureDir(mobileDir);
  const outPath = path.join(mobileDir, `${slug}-mobile.jpg`);
  await page.screenshot({
    path: outPath,
    fullPage: true,
    type: "jpeg",
    quality: args.quality,
    animations: "disabled",
  });

  await context.close();
  return { kind: "mobile", path: outPath, report };
}

async function getSectionMeta(handle) {
  return handle.evaluate((el) => {
    const rect = el.getBoundingClientRect();
    const heading = el.querySelector("h1, h2, h3, [data-title]")?.textContent?.trim();
    const className = String(el.className || "").split(/\s+/).filter(Boolean)[0];
    const label =
      el.getAttribute("data-export-section") ||
      el.getAttribute("aria-label") ||
      el.id ||
      heading ||
      className ||
      el.tagName.toLowerCase();

    return {
      label,
      width: rect.width,
      height: rect.height,
      top: rect.top + window.scrollY,
      visible: rect.width > 20 && rect.height > 40,
    };
  });
}

async function captureSections({ browser, url, outDir, args }) {
  const context = await browser.newContext({
    viewport: { width: args.mobileWidth, height: args.viewportHeight },
    deviceScaleFactor: args.scale,
    isMobile: true,
  });
  const page = await openReadyPage(context, url);
  const report = await inspectPage(page);
  const sectionDir = path.join(outDir, "sections");
  await ensureDir(sectionDir);

  const handles = await page.$$(args.sectionSelector);
  const captures = [];
  let index = 1;

  for (const handle of handles) {
    const meta = await getSectionMeta(handle);
    if (!meta.visible) continue;

    const outPath = path.join(sectionDir, fileNameFor(index, meta.label));
    await handle.screenshot({
      path: outPath,
      type: "jpeg",
      quality: args.quality,
      animations: "disabled",
    });
    captures.push({ path: outPath, label: meta.label, width: Math.round(meta.width), height: Math.round(meta.height) });
    index += 1;
  }

  await context.close();
  return { kind: "sections", count: captures.length, captures, report };
}

async function captureThumbnail({ browser, url, outDir, slug, args }) {
  const context = await browser.newContext({
    viewport: { width: args.thumbSize, height: args.thumbSize },
    deviceScaleFactor: args.scale,
  });
  const page = await openReadyPage(context, url);
  const report = await inspectPage(page);
  const thumbDir = path.join(outDir, "thumbnail");
  await ensureDir(thumbDir);
  const outPath = path.join(thumbDir, `${slug}-thumbnail-square.jpg`);

  await page.screenshot({
    path: outPath,
    type: "jpeg",
    quality: args.quality,
    clip: { x: 0, y: 0, width: args.thumbSize, height: args.thumbSize },
    animations: "disabled",
  });

  await context.close();
  return { kind: "thumbnail", path: outPath, report };
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  if (!args.html) {
    console.error("필수 옵션이 없습니다: --html /path/to/page.html");
    process.exit(2);
  }

  const htmlInput = expandHome(String(args.html));
  const url = toPageUrl(htmlInput);
  const outDir = path.resolve(expandHome(args.out || defaultOutDir(htmlInput)));
  const slug = slugify(args.slug || path.basename(htmlInput, path.extname(htmlInput)) || "event-page");
  await ensureDir(outDir);

  const { chromium } = await loadPlaywright();
  const browser = await chromium.launch({ headless: true });
  const results = [];

  try {
    if (args.mode === "page" || args.mode === "all") {
      results.push(await captureMobile({ browser, url, outDir, slug, args }));
    }
    if (args.mode === "sections" || args.mode === "all") {
      results.push(await captureSections({ browser, url, outDir, args }));
    }
    if (args.mode === "thumb" || args.mode === "thumbnail") {
      results.push(await captureThumbnail({ browser, url, outDir, slug, args }));
    }
  } finally {
    await browser.close();
  }

  const report = {
    input: htmlInput,
    url,
    outDir,
    mode: args.mode,
    mobileWidth: args.mobileWidth,
    scale: args.scale,
    quality: args.quality,
    createdAt: new Date().toISOString(),
    results,
  };
  await fs.writeFile(path.join(outDir, "export-report.json"), JSON.stringify(report, null, 2), "utf8");

  const warnings = results.flatMap((result) => {
    const pageReport = result.report || {};
    const items = [];
    if (pageReport.brokenImages?.length) items.push(`${result.kind}: broken images ${pageReport.brokenImages.length}`);
    if (pageReport.horizontalOverflow) items.push(`${result.kind}: horizontal overflow`);
    if (pageReport.textOverflow?.length) items.push(`${result.kind}: text overflow candidates ${pageReport.textOverflow.length}`);
    return items;
  });

  console.log(JSON.stringify({
    outDir,
    files: results.map((result) => result.path || `${result.count} section files`),
    warnings,
  }, null, 2));

  if (args.strict && warnings.length) {
    process.exitCode = 1;
  }
}

main().catch((error) => {
  console.error(error?.stack || error);
  process.exit(1);
});
