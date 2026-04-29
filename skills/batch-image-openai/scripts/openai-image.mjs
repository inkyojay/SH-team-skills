#!/usr/bin/env node

/**
 * Batch Image OpenAI — gpt-image-2 batch generation/edit
 *
 * 4 modes:
 *   1. Generate: 빈 폴더에서 프롬프트 → N개 새 이미지
 *   2. Edit: 입력 폴더 이미지 + 프롬프트 → 변환
 *   3. Reference: 레퍼런스 이미지 분석 → 같은 스타일로 입력 폴더 변환
 *   4. HTML: 상세페이지 HTML에서 컨셉 추출 → 입력 폴더 변환
 *
 * Usage:
 *   # Mode 1 — Generate
 *   node openai-image.mjs --generate --prompt "감성적인 아기 침대 라이프스타일 컷" \
 *     --n 5 --size 1024x1536 --output ./out
 *
 *   # Mode 2 — Edit
 *   node openai-image.mjs --edit --input ./photos --prompt "따뜻한 황금빛 자연광"
 *
 *   # Mode 3 — Reference
 *   node openai-image.mjs --edit --input ./photos --reference ./mood.png
 *
 *   # Mode 4 — HTML
 *   node openai-image.mjs --edit --input ./photos --html ./detail.html
 *
 * Common Options:
 *   --output <dir>           기본: <input>-output (edit) | ./out (generate)
 *   --model <id>             기본: gpt-image-2
 *   --size <WxH>             1024x1024 | 1536x1024 | 1024x1536 | auto (기본: 1024x1024)
 *   --quality <level>        low | medium | high | auto (기본: medium)
 *   --n <count>              생성 개수 (generate 모드, 기본: 1)
 *   --concurrency <n>        동시 처리 수 (기본: 2)
 *   --format <ext>           png | jpeg | webp (기본: png)
 *   --transparent            투명 배경 (PNG/WebP만)
 *   --prompt-only            실제 호출 안 하고 프롬프트만 출력 (dry-run)
 *
 * Env:
 *   OPENAI_API_KEY (필수)
 *   OPENAI_ORG (선택)
 */

import OpenAI from "openai";
import fs from "fs/promises";
import path from "path";

// ─────────────────────────────────────────────
// OpenAI Client
// ─────────────────────────────────────────────

let client = null;

function getClient() {
  if (client) return client;
  const apiKey = process.env.OPENAI_API_KEY;
  if (!apiKey) {
    console.error("[ERROR] OPENAI_API_KEY 환경변수가 필요합니다.");
    console.error("        export OPENAI_API_KEY='sk-...'");
    process.exit(1);
  }
  client = new OpenAI({
    apiKey,
    organization: process.env.OPENAI_ORG,
  });
  return client;
}

// ─────────────────────────────────────────────
// 가격 테이블 (USD per image, gpt-image-2)
// ─────────────────────────────────────────────

const PRICING = {
  "1024x1024": { low: 0.006, medium: 0.053, high: 0.211 },
  "1536x1024": { low: 0.005, medium: 0.041, high: 0.165 },
  "1024x1536": { low: 0.005, medium: 0.041, high: 0.165 },
};

function estimateCost(size, quality, n = 1) {
  const tier = PRICING[size];
  if (!tier) return null;
  const q = quality === "auto" ? "medium" : quality;
  const unit = tier[q] ?? tier.medium;
  return unit * n;
}

// ─────────────────────────────────────────────
// 한글 → 영어 번역 (OpenAI gpt-4o-mini 사용)
// ─────────────────────────────────────────────

async function translateToEnglish(text) {
  if (!/[가-힣]/.test(text)) return text;
  const ai = getClient();
  try {
    const res = await ai.chat.completions.create({
      model: "gpt-4o-mini",
      messages: [
        { role: "system", content: "Translate Korean to English. Return only the translation, nothing else." },
        { role: "user", content: text },
      ],
      max_tokens: 500,
    });
    return res.choices[0]?.message?.content?.trim() || text;
  } catch (e) {
    console.warn(`[WARN] 번역 실패, 원문 사용: ${e.message}`);
    return text;
  }
}

// ─────────────────────────────────────────────
// Reference 이미지 분석 → 프롬프트 추출
// ─────────────────────────────────────────────

async function analyzeReference(imagePath) {
  const ai = getClient();
  const buffer = await fs.readFile(imagePath);
  const base64 = buffer.toString("base64");
  const ext = path.extname(imagePath).slice(1).toLowerCase();
  const mime = `image/${ext === "jpg" ? "jpeg" : ext}`;

  const res = await ai.chat.completions.create({
    model: "gpt-4o-mini",
    messages: [
      {
        role: "user",
        content: [
          { type: "text", text: "Analyze this reference image and write a detailed prompt (English, 100-150 words) describing: (1) lighting/atmosphere, (2) color palette, (3) background/setting, (4) overall style/mood. Return ONLY the prompt text." },
          { type: "image_url", image_url: { url: `data:${mime};base64,${base64}` } },
        ],
      },
    ],
    max_tokens: 400,
  });
  return res.choices[0]?.message?.content?.trim() || "";
}

// ─────────────────────────────────────────────
// HTML에서 촬영 컨셉 추출
// ─────────────────────────────────────────────

async function extractFromHtml(htmlPath) {
  const ai = getClient();
  const html = await fs.readFile(htmlPath, "utf-8");
  // alt/title/heading만 추려 토큰 절약
  const summary = html
    .replace(/<style[\s\S]*?<\/style>/gi, "")
    .replace(/<script[\s\S]*?<\/script>/gi, "")
    .replace(/<[^>]+>/g, " ")
    .replace(/\s+/g, " ")
    .slice(0, 3000);

  const res = await ai.chat.completions.create({
    model: "gpt-4o-mini",
    messages: [
      {
        role: "user",
        content: `다음은 상세페이지 텍스트입니다. 이 페이지의 분위기/제품 컨셉을 잘 표현하는 영문 이미지 생성 프롬프트(100~150 단어)를 작성하세요. 조명/색감/배경/스타일 포함. 프롬프트만 반환:\n\n${summary}`,
      },
    ],
    max_tokens: 400,
  });
  return res.choices[0]?.message?.content?.trim() || "";
}

// ─────────────────────────────────────────────
// 동시 실행 헬퍼
// ─────────────────────────────────────────────

async function runConcurrent(items, limit, fn) {
  const results = [];
  for (let i = 0; i < items.length; i += limit) {
    const chunk = items.slice(i, i + limit);
    const r = await Promise.all(chunk.map(fn));
    results.push(...r);
  }
  return results;
}

// ─────────────────────────────────────────────
// Generate 모드
// ─────────────────────────────────────────────

async function generateMode(opts) {
  const { prompt, n, size, quality, output, model, format, transparent } = opts;
  const ai = getClient();

  const enPrompt = await translateToEnglish(prompt);
  console.log(`📝 Prompt: ${enPrompt.slice(0, 100)}${enPrompt.length > 100 ? "..." : ""}`);

  const cost = estimateCost(size, quality, n);
  console.log(`💰 예상 비용: ~$${cost?.toFixed(3) ?? "?"} (${n}개 × ${size} ${quality})`);

  await fs.mkdir(output, { recursive: true });

  const params = {
    model,
    prompt: enPrompt,
    size,
    quality,
    n: 1,  // gpt-image-2는 한 요청당 1장 (n>1은 병렬로)
    output_format: format,
  };
  if (transparent) {
    params.background = "transparent";
    if (format !== "png" && format !== "webp") {
      console.warn("[WARN] transparent는 png/webp만 지원. format을 png로 변경.");
      params.output_format = "png";
    }
  }

  let success = 0;
  const tasks = Array.from({ length: n }, (_, i) => i);
  await runConcurrent(tasks, opts.concurrency, async (i) => {
    try {
      const t0 = Date.now();
      const res = await ai.images.generate(params);
      const b64 = res.data[0]?.b64_json;
      if (!b64) throw new Error("no b64_json in response");
      const ext = params.output_format || "png";
      const fname = `gen_${String(i + 1).padStart(3, "0")}.${ext}`;
      const fpath = path.join(output, fname);
      await fs.writeFile(fpath, Buffer.from(b64, "base64"));
      success++;
      const ms = Date.now() - t0;
      console.log(`  ✓ [${i + 1}/${n}] ${fname} (${ms}ms)`);
    } catch (e) {
      console.error(`  ✗ [${i + 1}/${n}] ${e.message}`);
    }
  });

  console.log(`\n🎉 ${success}/${n} 완료 → ${output}`);
}

// ─────────────────────────────────────────────
// Edit 모드 (입력 폴더의 이미지를 프롬프트로 변환)
// ─────────────────────────────────────────────

async function editMode(opts) {
  const { input, prompt, output, size, quality, model, concurrency } = opts;
  const ai = getClient();

  const enPrompt = await translateToEnglish(prompt);
  console.log(`📝 Edit Prompt: ${enPrompt.slice(0, 100)}${enPrompt.length > 100 ? "..." : ""}`);

  const files = (await fs.readdir(input)).filter(f =>
    /\.(jpg|jpeg|png|webp)$/i.test(f)
  );
  if (files.length === 0) {
    console.error(`[ERROR] 입력 폴더에 이미지 없음: ${input}`);
    process.exit(1);
  }
  console.log(`📂 입력: ${files.length}장 (${input})`);

  const cost = estimateCost(size, quality, files.length);
  console.log(`💰 예상 비용: ~$${cost?.toFixed(3) ?? "?"} (${files.length}장 × ${size} ${quality})`);

  await fs.mkdir(output, { recursive: true });

  // OpenAI SDK v4의 images.edit는 file-like 객체 받음
  const { toFile } = await import("openai");

  let success = 0;
  await runConcurrent(files, concurrency, async (fname) => {
    const inPath = path.join(input, fname);
    try {
      const t0 = Date.now();
      const buf = await fs.readFile(inPath);
      const ext = path.extname(fname).slice(1).toLowerCase();
      const mime = `image/${ext === "jpg" ? "jpeg" : ext}`;
      const file = await toFile(buf, fname, { type: mime });

      const res = await ai.images.edit({
        model,
        image: file,
        prompt: enPrompt,
        size,
        quality,
        n: 1,
      });
      const b64 = res.data[0]?.b64_json;
      if (!b64) throw new Error("no b64_json");
      const stem = path.basename(fname, path.extname(fname));
      const outName = `${stem}-transformed.png`;
      const outPath = path.join(output, outName);
      await fs.writeFile(outPath, Buffer.from(b64, "base64"));
      success++;
      const ms = Date.now() - t0;
      console.log(`  ✓ ${fname} → ${outName} (${ms}ms)`);
    } catch (e) {
      console.error(`  ✗ ${fname}: ${e.message}`);
    }
  });

  console.log(`\n🎉 ${success}/${files.length} 완료 → ${output}`);
}

// ─────────────────────────────────────────────
// CLI 파서
// ─────────────────────────────────────────────

function parseArgs() {
  const args = process.argv.slice(2);
  const out = {
    mode: null,                  // "generate" | "edit"
    input: null,
    output: null,
    prompt: null,
    reference: null,
    html: null,
    model: "gpt-image-2",
    size: "1024x1024",
    quality: "medium",
    n: 1,
    concurrency: 2,
    format: "png",
    transparent: false,
    promptOnly: false,
  };
  for (let i = 0; i < args.length; i++) {
    const k = args[i];
    const next = args[i + 1];
    switch (k) {
      case "--generate": out.mode = "generate"; break;
      case "--edit":     out.mode = "edit"; break;
      case "--input":    out.input = next; i++; break;
      case "--output":   out.output = next; i++; break;
      case "--prompt":   out.prompt = next; i++; break;
      case "--reference":out.reference = next; i++; break;
      case "--html":     out.html = next; i++; break;
      case "--model":    out.model = next; i++; break;
      case "--size":     out.size = next; i++; break;
      case "--quality":  out.quality = next; i++; break;
      case "--n":        out.n = parseInt(next, 10); i++; break;
      case "--concurrency": out.concurrency = parseInt(next, 10); i++; break;
      case "--format":   out.format = next; i++; break;
      case "--transparent": out.transparent = true; break;
      case "--prompt-only": out.promptOnly = true; break;
      case "-h": case "--help":
        printHelp();
        process.exit(0);
    }
  }
  return out;
}

function printHelp() {
  console.log(`
Batch Image OpenAI — gpt-image-2 batch generation/edit

Modes:
  --generate     빈 폴더에서 프롬프트로 새 이미지 N개 생성
  --edit         입력 폴더 이미지 + 프롬프트로 변환

Options:
  --input <dir>          입력 폴더 (edit 모드 필수)
  --output <dir>         출력 폴더 (기본: <input>-output 또는 ./out)
  --prompt "text"        텍스트 프롬프트 (한국어 자동 영문 번역)
  --reference <img>      레퍼런스 이미지 → 자동 분석 후 프롬프트 생성
  --html <file>          HTML 파일 → 자동 컨셉 추출 후 프롬프트 생성
  --model <id>           기본: gpt-image-2
  --size <WxH>           1024x1024 | 1536x1024 | 1024x1536 | auto
  --quality <level>      low | medium | high | auto (기본: medium)
  --n <count>            생성 개수 (generate, 기본: 1)
  --concurrency <n>      병렬 (기본: 2)
  --format <ext>         png | jpeg | webp (기본: png)
  --transparent          투명 배경 (png/webp)
  --prompt-only          실제 호출 안 하고 프롬프트만 출력

Env:
  OPENAI_API_KEY    (필수)
  OPENAI_ORG        (선택)

Examples:
  node openai-image.mjs --generate --prompt "감성 아기침대 라이프 컷" --n 5
  node openai-image.mjs --edit --input ./photos --prompt "황금빛 자연광"
  node openai-image.mjs --edit --input ./photos --reference ./mood.png
  node openai-image.mjs --edit --input ./photos --html ./detail.html
`);
}

// ─────────────────────────────────────────────
// Main
// ─────────────────────────────────────────────

async function main() {
  const opts = parseArgs();

  if (!opts.mode) {
    console.error("[ERROR] --generate 또는 --edit 모드 필요");
    printHelp();
    process.exit(1);
  }

  // 프롬프트 결정 (--reference, --html은 자동으로 prompt 생성)
  if (opts.reference) {
    console.log(`🔍 Reference 분석: ${opts.reference}`);
    const auto = await analyzeReference(opts.reference);
    opts.prompt = (opts.prompt ? opts.prompt + ". " : "") + auto;
  }
  if (opts.html) {
    console.log(`📄 HTML 컨셉 추출: ${opts.html}`);
    const auto = await extractFromHtml(opts.html);
    opts.prompt = (opts.prompt ? opts.prompt + ". " : "") + auto;
  }

  if (!opts.prompt) {
    console.error("[ERROR] --prompt, --reference, 또는 --html 중 하나 필요");
    process.exit(1);
  }

  if (opts.promptOnly) {
    console.log("\n=== Generated Prompt ===");
    console.log(opts.prompt);
    console.log("=== End ===");
    return;
  }

  // 출력 폴더 결정
  if (!opts.output) {
    if (opts.mode === "edit" && opts.input) {
      opts.output = `${opts.input.replace(/\/$/, "")}-output`;
    } else {
      opts.output = "./out";
    }
  }

  if (opts.mode === "generate") {
    await generateMode(opts);
  } else {
    if (!opts.input) {
      console.error("[ERROR] --edit 모드는 --input 필요");
      process.exit(1);
    }
    await editMode(opts);
  }
}

main().catch(e => {
  console.error("[FATAL]", e.message);
  if (process.env.DEBUG) console.error(e.stack);
  process.exit(1);
});
