#!/usr/bin/env node

/**
 * Batch Image Transform
 *
 * 상품 이미지를 배치로 변환합니다. Gemini AI로 배경 교체/톤 변환을 일괄 처리합니다.
 * 기존 코드 apps/dahae/app/features/image-generator/lib/gemini.server.ts 에서 포팅.
 *
 * Usage:
 *   node batch-transform.mjs --input <folder> --prompt "text" [options]
 *   node batch-transform.mjs --input <folder> --reference <image> [options]
 *   node batch-transform.mjs --input <folder> --html <file.html> [options]
 *
 * Options:
 *   --output <folder>         출력 폴더 (기본: <input>-output)
 *   --model <model>           gemini-3-pro | gemini-2.5-flash (기본: gemini-2.5-flash)
 *   --aspect-ratio <ratio>    1:1 | 9:16 | 16:9 (기본: 1:1)
 *   --concurrency <n>         동시 처리 수 (기본: 2)
 *   --appearance <text>       외모/인물 프롬프트 (선택)
 */

import { GoogleGenAI, Modality } from "@google/genai";
import fs from "fs/promises";
import path from "path";

// ─────────────────────────────────────────────
// Gemini Client
// ─────────────────────────────────────────────

let client = null;

function getClient() {
  if (client) return client;
  const apiKey = process.env.GOOGLE_AI_API_KEY;
  if (!apiKey) {
    console.error("[ERROR] GOOGLE_AI_API_KEY 환경변수가 필요합니다.");
    process.exit(1);
  }
  client = new GoogleGenAI({ apiKey });
  return client;
}

// ─────────────────────────────────────────────
// Translation (gemini.server.ts L35-61)
// ─────────────────────────────────────────────

async function translateToEnglish(text) {
  const hasKorean = /[가-힣]/.test(text);
  if (!hasKorean) return text;

  const ai = getClient();
  try {
    const response = await ai.models.generateContent({
      model: "gemini-2.0-flash",
      contents: [{
        role: "user",
        parts: [{
          text: `Translate the following Korean text to English. Only return the translated text, nothing else:\n\n"${text}"`
        }]
      }]
    });
    return response.candidates?.[0]?.content?.parts?.[0]?.text?.trim() || text;
  } catch {
    return text;
  }
}

// ─────────────────────────────────────────────
// Image Analysis (gemini.server.ts L250-325)
// ─────────────────────────────────────────────

async function analyzeImage(imageBase64, mimeType) {
  const ai = getClient();
  const prompt = `Analyze this image and generate a detailed prompt that could be used to recreate a similar scene in an AI image generator. Focus on:
1. Background setting and environment
2. Lighting conditions and atmosphere
3. Colors and textures
4. Style and mood
5. Any people or objects visible

Return TWO prompts separated by "|||":
BACKGROUND: [detailed background description 150-200 words]
|||
APPEARANCE: [person/subject description or empty]`;

  const response = await ai.models.generateContent({
    model: "gemini-2.0-flash",
    contents: [{
      role: "user",
      parts: [
        { inlineData: { mimeType, data: imageBase64 } },
        { text: prompt }
      ]
    }]
  });

  const text = response.candidates?.[0]?.content?.parts?.[0]?.text || "";
  const parts = text.split("|||");
  let backgroundPrompt = "";
  let appearancePrompt = "";

  if (parts.length >= 1) {
    const bgMatch = parts[0].match(/BACKGROUND:\s*(.*)/s);
    if (bgMatch) backgroundPrompt = bgMatch[1].trim();
  }
  if (parts.length >= 2) {
    const appMatch = parts[1].match(/APPEARANCE:\s*(.*)/s);
    if (appMatch) appearancePrompt = appMatch[1].trim();
  }
  if (!backgroundPrompt) {
    backgroundPrompt = text.replace(/BACKGROUND:|APPEARANCE:/g, "").trim();
  }

  return { backgroundPrompt, appearancePrompt };
}

// ─────────────────────────────────────────────
// HTML Analysis (Mode B)
// ─────────────────────────────────────────────

async function analyzeHtml(htmlContent) {
  const ai = getClient();
  const prompt = `이 상세페이지 HTML을 분석해서 이 상품에 필요한 촬영 컨셉을 파악하세요.

반환 형식 (JSON만, 마크다운 코드펜스 없이):
{
  "backgroundPrompt": "배경/환경/조명/분위기 상세 설명 (영문 150-200단어)",
  "appearancePrompt": "인물/모델 필요시 설명, 불필요하면 빈 문자열"
}`;

  const response = await ai.models.generateContent({
    model: "gemini-2.0-flash",
    contents: [{
      role: "user",
      parts: [{ text: prompt + "\n\n" + htmlContent }]
    }]
  });

  const text = response.candidates?.[0]?.content?.parts?.[0]?.text || "{}";
  const cleaned = text.replace(/```json\n?/g, "").replace(/```\n?/g, "").trim();
  try {
    return JSON.parse(cleaned);
  } catch {
    const match = cleaned.match(/\{[\s\S]*\}/);
    return match ? JSON.parse(match[0]) : { backgroundPrompt: cleaned, appearancePrompt: "" };
  }
}

// ─────────────────────────────────────────────
// Prompt Builder (gemini.server.ts L155-214)
// ─────────────────────────────────────────────

function getAspectRatioDescription(aspectRatio) {
  const descriptions = {
    "1:1": "square format (1:1 aspect ratio, equal width and height)",
    "9:16": "vertical/portrait format (9:16 aspect ratio, taller than wide, suitable for mobile stories and reels)",
    "16:9": "horizontal/landscape format (16:9 aspect ratio, wider than tall, suitable for YouTube and banners)",
  };
  return descriptions[aspectRatio] || descriptions["1:1"];
}

function buildPrompt(backgroundPrompt, appearancePrompt, aspectRatio = "1:1") {
  const aspectDescription = getAspectRatioDescription(aspectRatio);

  return `You are an image transformation engine that takes a product or subject photo shot in a plain studio or horizon background, a background description, and an optional appearance prompt.

Input Context:
- Background Description: "${backgroundPrompt}"
${appearancePrompt ? `- Appearance Prompt: "${appearancePrompt}"` : '- Appearance Prompt: None provided.'}
- Output Format: ${aspectDescription}

Your task is to generate a realistic, high-quality scene composite, placing the subject from the original photo into the described background environment.

Follow these strict rules:

1. Preserve the subject exactly as in the original photos:
   - Keep shape, proportions, product design, texture, materials, colors, logos, and details.
   - Do not alter the person's identity, body shape, clothing, hands, or pose unless directed by the appearance prompt.
   - Do not change the product's structure, edges, or silhouette.
   - Do not add or remove elements from the subject.

2. Apply the user's background description:
   - Replace the plain studio or horizon background with the background described by the user.
   - The subject must blend naturally into the new scene.
   - Match lighting direction, brightness, color temperature, shadows, and reflections.
   - Ensure realistic contact shadows or surface grounding when needed.
   - Never distort the subject to fit the scene.

3. Apply the appearance prompt (if provided):
   - Use the appearance prompt to define the look, style, facial characteristics, and overall vibe of any human figures in the final output.
   - All generated images must maintain consistent appearance for the people described, including hairstyle, facial features, age range, and general styling.
   - Never modify subjects beyond what is specifically described in the appearance prompt.
   - When no appearance prompt is provided, preserve the original appearance of all people in the input photos.

4. Specific Appearance Rules:
   - Appearance prompts define ONLY facial features, hairstyle, age, skin tone, and styling.
   - Actions, pose, gaze direction, or interaction must never be taken from the appearance prompt.
   - If the input image contains people, preserve their identity unless the appearance prompt explicitly contradicts it.
   - If the input image contains no people, but the appearance prompt describes people, generate those people and place them naturally into the described background along with the subject.

5. Composition and Format rules:
   - IMPORTANT: Generate the image in ${aspectDescription}. The output image dimensions must match this aspect ratio.
   - Maintain the original camera angle, subject scale, and framing unless the user requests otherwise.
   - For vertical formats, compose the scene to work well in portrait orientation.
   - For horizontal formats, compose the scene to work well in landscape orientation.
   - The final images must look like real photographs taken in the described environment.
   - Avoid artifacts, warping, double limbs, mesh distortion, or missing details.

Output: Return a high-quality photograph in ${aspectDescription}. Do not add text, borders, or watermarks.`;
}

// ─────────────────────────────────────────────
// Image Generation (gemini.server.ts L66-150)
// ─────────────────────────────────────────────

const IMAGE_MODELS = {
  "gemini-3-pro": "models/gemini-3-pro-image-preview",
  "gemini-2.5-flash": "models/gemini-2.5-flash-image",
};

async function generateScene(imageBase64, mimeType, backgroundPrompt, appearancePrompt, model = "gemini-3-pro", aspectRatio = "1:1") {
  const translatedBg = await translateToEnglish(backgroundPrompt);
  const translatedApp = appearancePrompt ? await translateToEnglish(appearancePrompt) : undefined;
  const systemPrompt = buildPrompt(translatedBg, translatedApp, aspectRatio);
  const ai = getClient();
  const modelId = IMAGE_MODELS[model] || IMAGE_MODELS["gemini-3-pro"];

  const response = await ai.models.generateContent({
    model: modelId,
    contents: [{
      role: "user",
      parts: [
        { inlineData: { mimeType, data: imageBase64 } },
        { text: systemPrompt },
      ]
    }],
    config: {
      responseModalities: [Modality.TEXT, Modality.IMAGE],
    },
  });

  const candidate = response.candidates?.[0];
  if (!candidate) {
    throw new Error("No response candidates from Gemini AI");
  }

  if (candidate.finishReason && candidate.finishReason !== "STOP" && candidate.finishReason !== "MAX_TOKENS") {
    throw new Error(`Image generation blocked: ${candidate.finishReason}`);
  }

  const parts = candidate.content?.parts || [];
  for (const part of parts) {
    if (part.inlineData?.data) {
      return { base64: part.inlineData.data, mimeType: part.inlineData.mimeType || "image/png" };
    }
  }

  // Log any text response for debugging
  for (const part of parts) {
    if (part.text) {
      console.warn("[Gemini] Model returned text:", part.text.substring(0, 200));
    }
  }

  throw new Error("No image data received from Gemini AI");
}

// ─────────────────────────────────────────────
// Utilities
// ─────────────────────────────────────────────

async function scanFolder(dirPath) {
  const entries = await fs.readdir(dirPath);
  const imageExts = [".jpg", ".jpeg", ".png", ".webp"];
  return entries
    .filter(f => imageExts.includes(path.extname(f).toLowerCase()))
    .sort()
    .map(f => path.join(dirPath, f));
}

async function imageToBase64(filePath) {
  const buffer = await fs.readFile(filePath);
  const ext = path.extname(filePath).toLowerCase();
  const mimeTypes = {
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".png": "image/png",
    ".webp": "image/webp",
  };
  return {
    base64: buffer.toString("base64"),
    mimeType: mimeTypes[ext] || "image/png",
  };
}

function sleep(ms) {
  return new Promise(r => setTimeout(r, ms));
}

function formatTime(seconds) {
  const m = Math.floor(seconds / 60);
  const s = Math.floor(seconds % 60);
  return m > 0 ? `${m}m ${s}s` : `${s}s`;
}

// ─────────────────────────────────────────────
// Single Image Processing
// ─────────────────────────────────────────────

async function processImage(filePath, bgPrompt, appPrompt, outputDir, model, aspectRatio, retries = 3) {
  const { base64, mimeType } = await imageToBase64(filePath);
  const fileName = path.basename(filePath, path.extname(filePath));

  for (let attempt = 1; attempt <= retries; attempt++) {
    try {
      const result = await generateScene(base64, mimeType, bgPrompt, appPrompt, model, aspectRatio);
      const ext = result.mimeType === "image/jpeg" ? ".jpg" : ".png";
      const outputPath = path.join(outputDir, `${fileName}-transformed${ext}`);
      await fs.writeFile(outputPath, Buffer.from(result.base64, "base64"));
      return { success: true, outputPath };
    } catch (error) {
      if (error.message?.includes("429") && attempt < retries) {
        const delay = Math.pow(2, attempt) * 5000;
        console.log(`  Rate limited. Retrying in ${delay / 1000}s...`);
        await sleep(delay);
        continue;
      }
      if (error.message?.includes("blocked") && attempt < retries) {
        console.log(`  Blocked by safety filter. Retrying (${attempt}/${retries})...`);
        await sleep(2000);
        continue;
      }
      return { success: false, error: error.message };
    }
  }
}

// ─────────────────────────────────────────────
// Batch Processing
// ─────────────────────────────────────────────

async function batchProcess(files, bgPrompt, appPrompt, outputDir, model, aspectRatio, concurrency = 2) {
  const results = { success: 0, failed: 0, failures: [] };
  const totalStart = Date.now();

  for (let i = 0; i < files.length; i += concurrency) {
    const batch = files.slice(i, i + concurrency);
    const promises = batch.map(async (file, j) => {
      const idx = i + j + 1;
      const name = path.basename(file);
      process.stdout.write(`[${idx}/${files.length}] ${name} ... `);
      const start = Date.now();
      const result = await processImage(file, bgPrompt, appPrompt, outputDir, model, aspectRatio);
      const elapsed = ((Date.now() - start) / 1000).toFixed(1);
      if (result.success) {
        console.log(`done (${elapsed}s) -> ${path.basename(result.outputPath)}`);
        results.success++;
      } else {
        console.log(`FAILED (${elapsed}s): ${result.error}`);
        results.failed++;
        results.failures.push({ file: name, error: result.error });
      }
    });
    await Promise.all(promises);

    // Brief delay between batches to avoid rate limiting
    if (i + concurrency < files.length) {
      await sleep(1000);
    }
  }

  results.totalTime = (Date.now() - totalStart) / 1000;
  return results;
}

// ─────────────────────────────────────────────
// Argument Parser
// ─────────────────────────────────────────────

function parseArgs() {
  const args = process.argv.slice(2);

  if (args.includes("--help") || args.includes("-h") || args.length === 0) {
    console.log(`
Usage:
  node batch-transform.mjs --input <folder> --prompt "text" [options]
  node batch-transform.mjs --input <folder> --reference <image> [options]
  node batch-transform.mjs --input <folder> --html <file.html> [options]

Modes:
  --prompt <text>        직접 배경 프롬프트 입력 (Mode C)
  --reference <image>    레퍼런스 이미지에서 프롬프트 추출 (Mode A)
  --html <file>          HTML 상세페이지에서 컨셉 추출 (Mode B)

Options:
  --output <folder>      출력 폴더 (기본: <input>-output)
  --model <model>        gemini-3-pro | gemini-2.5-flash (기본: gemini-2.5-flash)
  --aspect-ratio <ratio> 1:1 | 9:16 | 16:9 (기본: 1:1)
  --appearance <text>    외모/인물 프롬프트 (선택)
  --concurrency <n>      동시 처리 수 (기본: 2)
  --help                 도움말 표시
`);
    process.exit(0);
  }

  const parsed = {
    input: null,
    output: null,
    reference: null,
    html: null,
    prompt: null,
    appearance: null,
    model: "gemini-2.5-flash",
    aspectRatio: "1:1",
    concurrency: 2,
  };

  for (let i = 0; i < args.length; i++) {
    switch (args[i]) {
      case "--input": parsed.input = args[++i]; break;
      case "--output": parsed.output = args[++i]; break;
      case "--reference": parsed.reference = args[++i]; break;
      case "--html": parsed.html = args[++i]; break;
      case "--prompt": parsed.prompt = args[++i]; break;
      case "--appearance": parsed.appearance = args[++i]; break;
      case "--model": parsed.model = args[++i]; break;
      case "--aspect-ratio": parsed.aspectRatio = args[++i]; break;
      case "--concurrency": parsed.concurrency = parseInt(args[++i]); break;
    }
  }

  if (!parsed.input) {
    console.error("[ERROR] --input <folder> is required");
    process.exit(1);
  }
  if (!parsed.reference && !parsed.html && !parsed.prompt) {
    console.error("[ERROR] One of --reference, --html, or --prompt is required");
    process.exit(1);
  }

  // Validate model
  if (!IMAGE_MODELS[parsed.model]) {
    console.error(`[ERROR] Invalid model: ${parsed.model}. Use: gemini-3-pro | gemini-2.5-flash`);
    process.exit(1);
  }

  // Validate aspect ratio
  const validRatios = ["1:1", "9:16", "16:9"];
  if (!validRatios.includes(parsed.aspectRatio)) {
    console.error(`[ERROR] Invalid aspect ratio: ${parsed.aspectRatio}. Use: 1:1 | 9:16 | 16:9`);
    process.exit(1);
  }

  return parsed;
}

// ─────────────────────────────────────────────
// Main
// ─────────────────────────────────────────────

async function main() {
  const args = parseArgs();

  console.log("\n========================================");
  console.log("  Batch Image Transform");
  console.log("========================================\n");

  // 1. Scan input folder
  const files = await scanFolder(args.input);
  if (files.length === 0) {
    console.error(`[ERROR] No images found in: ${args.input}`);
    console.error("  Supported formats: .jpg, .jpeg, .png, .webp");
    process.exit(1);
  }

  // 2. Determine prompts based on mode
  let bgPrompt;
  let appPrompt = args.appearance || "";

  if (args.reference) {
    console.log("[Mode A] Analyzing reference image...");
    const { base64, mimeType } = await imageToBase64(args.reference);
    const analysis = await analyzeImage(base64, mimeType);
    bgPrompt = analysis.backgroundPrompt;
    if (!appPrompt && analysis.appearancePrompt) {
      appPrompt = analysis.appearancePrompt;
    }
    console.log("[Mode A] Analysis complete.\n");
  } else if (args.html) {
    console.log("[Mode B] Analyzing HTML detail page...");
    const htmlContent = await fs.readFile(args.html, "utf-8");
    const analysis = await analyzeHtml(htmlContent);
    bgPrompt = analysis.backgroundPrompt;
    if (!appPrompt && analysis.appearancePrompt) {
      appPrompt = analysis.appearancePrompt;
    }
    console.log("[Mode B] Analysis complete.\n");
  } else {
    console.log("[Mode C] Using direct prompt.\n");
    bgPrompt = args.prompt;
  }

  // 3. Display config
  console.log(`[Config] Input:       ${args.input} (${files.length} images)`);
  console.log(`[Config] Model:       ${args.model}`);
  console.log(`[Config] Aspect:      ${args.aspectRatio}`);
  console.log(`[Config] Concurrency: ${args.concurrency}`);
  console.log(`[Prompt] Background:  "${bgPrompt.length > 80 ? bgPrompt.substring(0, 80) + "..." : bgPrompt}"`);
  if (appPrompt) {
    console.log(`[Prompt] Appearance:  "${appPrompt.length > 80 ? appPrompt.substring(0, 80) + "..." : appPrompt}"`);
  }

  // 4. Create output directory
  const outputDir = args.output || args.input + "-output";
  await fs.mkdir(outputDir, { recursive: true });
  console.log(`[Output] ${outputDir}/`);
  console.log("");

  // 5. Batch process
  const results = await batchProcess(files, bgPrompt, appPrompt, outputDir, args.model, args.aspectRatio, args.concurrency);

  // 6. Summary
  console.log("\n========================================");
  console.log("  Summary");
  console.log("========================================");
  console.log(`  Total:     ${files.length} images`);
  console.log(`  Success:   ${results.success}`);
  console.log(`  Failed:    ${results.failed}`);
  console.log(`  Time:      ${formatTime(results.totalTime)}`);
  console.log(`  Output:    ${outputDir}/`);

  if (results.failures.length > 0) {
    console.log("\n  Failed files:");
    results.failures.forEach(f => console.log(`    - ${f.file}: ${f.error}`));
  }

  console.log("");
}

main().catch(err => {
  console.error("[FATAL]", err);
  process.exit(1);
});
