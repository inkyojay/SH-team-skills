import { GoogleGenAI, Modality } from "@google/genai";
import sharp from "sharp";
import fs from "fs/promises";
import path from "path";

// ── Client ──────────────────────────────────────────────

let client = null;
function getClient() {
  if (client) return client;
  const apiKey = process.env.GOOGLE_AI_API_KEY;
  if (!apiKey) {
    console.error("[ERROR] GOOGLE_AI_API_KEY 환경변수가 설정되지 않았습니다.");
    process.exit(1);
  }
  client = new GoogleGenAI({ apiKey });
  return client;
}

// ── Models ──────────────────────────────────────────────

const MODELS = {
  "gemini-2.5-flash": { id: "models/gemini-2.5-flash-image", name: "Gemini 2.5 Flash" },
  "gemini-3-pro": { id: "models/gemini-3-pro-image-preview", name: "Gemini 3 Pro" },
};

// ── Prompt (ported from tone-match.tsx L23-26) ──────────

function buildToneMatchPrompt(intensity) {
  return `Apply the color grading and tone of the Reference Image to the Source Image.
Keep the Source Image content, composition, framing, and dimensions 100% identical.
Only change colors, mood, and color grading. Do NOT alter the layout, crop, or aspect ratio.
Intensity: ${intensity}% (0=no change, 100=full change)
Output ONLY the processed image at the same resolution as the Source Image.`;
}

// ── Pre-process reference to match source aspect ratio ──

async function prepareReference(refBuffer, sourceWidth, sourceHeight) {
  const refMeta = await sharp(refBuffer).metadata();
  const sourceRatio = sourceWidth / sourceHeight;
  const refRatio = refMeta.width / refMeta.height;

  // If aspect ratios differ significantly, crop reference to match source ratio
  // This prevents Gemini from adopting the reference's aspect ratio
  if (Math.abs(sourceRatio - refRatio) > 0.15) {
    console.log(`[Reference] Cropping to match source ratio (${sourceRatio.toFixed(2)} vs ${refRatio.toFixed(2)})`);
    let cropWidth, cropHeight;
    if (refRatio > sourceRatio) {
      // Reference is wider → crop width
      cropHeight = refMeta.height;
      cropWidth = Math.round(cropHeight * sourceRatio);
    } else {
      // Reference is taller → crop height
      cropWidth = refMeta.width;
      cropHeight = Math.round(cropWidth / sourceRatio);
    }
    const cropped = await sharp(refBuffer)
      .extract({
        left: Math.round((refMeta.width - cropWidth) / 2),
        top: Math.round((refMeta.height - cropHeight) / 2),
        width: cropWidth,
        height: cropHeight,
      })
      .png()
      .toBuffer();
    return { base64: cropped.toString("base64"), mimeType: "image/png" };
  }

  return { base64: refBuffer.toString("base64"), mimeType: "image/png" };
}

// ── Single tone match (ported from tone-match.tsx L31-60) ──

async function processSingleToneMatch(
  originalBase64, originalMimeType,
  referenceBase64, referenceMimeType,
  intensity, modelId
) {
  const ai = getClient();
  const response = await ai.models.generateContent({
    model: modelId,
    contents: {
      parts: [
        { text: buildToneMatchPrompt(intensity) },
        { text: "Source Image:" },
        { inlineData: { mimeType: originalMimeType, data: originalBase64 } },
        { text: "Reference Image:" },
        { inlineData: { mimeType: referenceMimeType, data: referenceBase64 } },
      ],
    },
    config: { responseModalities: [Modality.IMAGE] },
  });

  const part = response.candidates?.[0]?.content?.parts?.[0];
  if (part?.inlineData?.data) {
    return { base64: part.inlineData.data, mimeType: part.inlineData.mimeType || "image/png" };
  }
  throw new Error("No image data returned from Gemini");
}

// ── Utilities ───────────────────────────────────────────

async function scanFolder(dirPath) {
  const entries = await fs.readdir(dirPath);
  const imageExts = [".jpg", ".jpeg", ".png", ".webp"];
  return entries
    .filter(f => imageExts.includes(path.extname(f).toLowerCase()))
    .sort()
    .map(f => path.join(dirPath, f));
}

function sleep(ms) {
  return new Promise(r => setTimeout(r, ms));
}

// ── Process single image (with 429 retry) ───────────────

async function processImage(filePath, refBuffer, intensity, modelId, outputDir, retries = 3) {
  const srcBuffer = await fs.readFile(filePath);
  const srcMeta = await sharp(srcBuffer).metadata();
  const srcWidth = srcMeta.width;
  const srcHeight = srcMeta.height;
  const ext = path.extname(filePath).toLowerCase();
  const mimeTypes = { ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".png": "image/png", ".webp": "image/webp" };
  const srcMimeType = mimeTypes[ext] || "image/png";
  const srcBase64 = srcBuffer.toString("base64");

  // Pre-process reference to match this source's aspect ratio
  const ref = await prepareReference(refBuffer, srcWidth, srcHeight);
  const fileName = path.basename(filePath, path.extname(filePath));

  for (let attempt = 1; attempt <= retries; attempt++) {
    try {
      const result = await processSingleToneMatch(
        srcBase64, srcMimeType,
        ref.base64, ref.mimeType,
        intensity, modelId
      );

      // Post-process: ensure output matches source dimensions exactly
      let outputBuffer = Buffer.from(result.base64, "base64");
      const outMeta = await sharp(outputBuffer).metadata();

      if (outMeta.width !== srcWidth || outMeta.height !== srcHeight) {
        console.log(`  [resize ${outMeta.width}x${outMeta.height} → ${srcWidth}x${srcHeight}]`);
        outputBuffer = await sharp(outputBuffer)
          .resize(srcWidth, srcHeight, { fit: "cover", position: "center" })
          .png()
          .toBuffer();
      }

      const outputPath = path.join(outputDir, `${fileName}-toned.png`);
      await fs.writeFile(outputPath, outputBuffer);
      return { success: true, outputPath };
    } catch (error) {
      if ((error.message?.includes("429") || error.message?.includes("quota")) && attempt < retries) {
        const delay = Math.pow(2, attempt) * 5000;
        console.log(`  Rate limited. Retrying in ${delay / 1000}s...`);
        await sleep(delay);
        continue;
      }
      return { success: false, error: error.message };
    }
  }
  return { success: false, error: "Max retries exceeded" };
}

// ── Batch processing (concurrency control) ──────────────

async function batchProcess(files, refBuffer, intensity, modelId, outputDir, concurrency = 2) {
  const results = { success: 0, failed: 0, failures: [] };

  for (let i = 0; i < files.length; i += concurrency) {
    const batch = files.slice(i, i + concurrency);
    const promises = batch.map(async (file, j) => {
      const idx = i + j + 1;
      const name = path.basename(file);
      process.stdout.write(`[${idx}/${files.length}] ${name} ... `);

      const start = Date.now();
      const result = await processImage(file, refBuffer, intensity, modelId, outputDir);

      if (result.success) {
        console.log(`done (${((Date.now() - start) / 1000).toFixed(1)}s)`);
        results.success++;
      } else {
        console.log(`FAILED: ${result.error}`);
        results.failed++;
        results.failures.push({ file: name, error: result.error });
      }
    });
    await Promise.all(promises);

    if (i + concurrency < files.length) {
      await sleep(1000);
    }
  }

  return results;
}

// ── CLI args ────────────────────────────────────────────

function parseArgs() {
  const args = process.argv.slice(2);
  const parsed = {
    reference: null,
    input: null,
    output: null,
    intensity: 70,
    model: "gemini-2.5-flash",
    concurrency: 2,
  };

  for (let i = 0; i < args.length; i++) {
    switch (args[i]) {
      case "--reference": parsed.reference = args[++i]; break;
      case "--input": parsed.input = args[++i]; break;
      case "--output": parsed.output = args[++i]; break;
      case "--intensity": parsed.intensity = Math.max(0, Math.min(100, parseInt(args[++i]))); break;
      case "--model": parsed.model = args[++i]; break;
      case "--concurrency": parsed.concurrency = Math.max(1, parseInt(args[++i])); break;
      case "--help":
        console.log(`Usage: node batch-tone-match.mjs [options]

  --reference <path>    Reference image (tone source) [required]
  --input <folder>      Product images folder [required]
  --output <folder>     Output folder (default: {input}-toned)
  --intensity <0-100>   Tone intensity (default: 70)
  --model <name>        gemini-2.5-flash | gemini-3-pro (default: gemini-2.5-flash)
  --concurrency <n>     Parallel count (default: 2)`);
        process.exit(0);
    }
  }

  if (!parsed.reference) {
    console.error("[ERROR] --reference is required");
    process.exit(1);
  }
  if (!parsed.input) {
    console.error("[ERROR] --input is required");
    process.exit(1);
  }

  return parsed;
}

// ── Main ────────────────────────────────────────────────

async function main() {
  const args = parseArgs();
  const modelConfig = MODELS[args.model] || MODELS["gemini-2.5-flash"];

  console.log("\n========================================");
  console.log("  Tone Match Local");
  console.log("========================================\n");

  // 1. Load reference as raw buffer (will be cropped per-source later)
  console.log(`[Reference] Loading ${args.reference}...`);
  const refBuffer = await fs.readFile(args.reference);
  const refMeta = await sharp(refBuffer).metadata();
  console.log(`[Reference] Loaded (${refMeta.width}x${refMeta.height})\n`);

  // 2. Scan input
  const files = await scanFolder(args.input);
  if (files.length === 0) {
    console.error("[ERROR] No images found in input folder");
    process.exit(1);
  }

  // 3. Config
  console.log(`[Config] Input:     ${args.input} (${files.length} images)`);
  console.log(`[Config] Model:     ${modelConfig.name}`);
  console.log(`[Config] Intensity: ${args.intensity}%`);
  console.log(`[Config] Parallel:  ${args.concurrency}`);

  // 4. Output dir
  const outputDir = args.output || args.input + "-toned";
  await fs.mkdir(outputDir, { recursive: true });
  console.log(`[Config] Output:    ${outputDir}/\n`);

  // 5. Batch
  const results = await batchProcess(
    files, refBuffer,
    args.intensity, modelConfig.id, outputDir, args.concurrency
  );

  // 6. Summary
  console.log("\n========================================");
  console.log(`  Results: ${results.success} succeeded, ${results.failed} failed`);
  console.log(`  Output:  ${outputDir}/`);
  if (results.failures.length > 0) {
    console.log("  Failures:");
    results.failures.forEach(f => console.log(`    - ${f.file}: ${f.error}`));
  }
  console.log("========================================\n");
}

main().catch(err => {
  console.error("[FATAL]", err.message || err);
  process.exit(1);
});
