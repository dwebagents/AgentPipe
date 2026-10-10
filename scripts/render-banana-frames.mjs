#!/usr/bin/env node
/**
 * Pre-render deterministic full-resolution PNG frames of the 4D banana
 * simulation (issue #149).
 *
 * Why: the animated canvas is invisible to screen readers. This script renders
 * the exact same deterministic frames the live animation draws and writes them
 * as full resolution PNGs that are embedded in the DOM (at opacity 0) with
 * descriptive alt text, so assistive technology can inspect the simulation.
 *
 * How it works:
 *   1. Load docs/index.html in headless Chromium (the shipped page).
 *   2. For each frame timestamp, call window.AgentPipeBanana4D.renderTo() —
 *      the exact renderer the live canvas uses — on an offscreen canvas sized
 *      760x560 CSS pixels at devicePixelRatio 2 (=> 1520x1120 PNG pixels).
 *   3. Save each frame plus a manifest with sha256 checksums, so tests can
 *      verify the committed frames are the genuine, reproducible output.
 *
 * Usage:
 *   export NODE_PATH="$(npm root -g)"   # where playwright lives
 *   node scripts/render-banana-frames.mjs               # render frames
 *   node scripts/render-banana-frames.mjs --optimize    # + palette-compress PNGs (needs sharp)
 *
 * The output is deterministic: same code + same seed + same timestamps
 * always produce the same pixels.
 */

import { createHash } from "node:crypto";
import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import { createRequire } from "node:module";

const require = createRequire(import.meta.url);

let playwright;
try {
  playwright = require("playwright");
} catch (error) {
  console.error(
    "playwright is required. Install it globally and set NODE_PATH, e.g.:\n" +
      '  export NODE_PATH="$(npm root -g)"\n',
  );
  process.exit(1);
}

const optimize = process.argv.includes("--optimize");
const root = join(dirname(fileURLToPath(import.meta.url)), "..");
const outDir = join(root, "docs", "assets", "banana-frames");

const SEED = 314159;
const CSS_WIDTH = 760;
const CSS_HEIGHT = 560;
const DPR = 2;
const FRAME_COUNT = 12;
const INTERVAL_SECONDS = 0.5;

function sha256(buffer) {
  return createHash("sha256").update(buffer).digest("hex");
}

/** Read PNG width/height from the IHDR chunk (no image library needed). */
function pngDimensions(buffer) {
  const signature = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);
  if (!buffer.subarray(0, 8).equals(signature)) {
    throw new Error("not a PNG file");
  }
  return { width: buffer.readUInt32BE(16), height: buffer.readUInt32BE(20) };
}

async function optimizePng(buffer) {
  let sharp;
  try {
    sharp = require("sharp");
  } catch {
    console.error(
      "--optimize requires sharp (npm install -g sharp, or run without --optimize).",
    );
    process.exit(1);
  }
  return sharp(buffer)
    .png({ palette: true, quality: 92, effort: 9 })
    .toBuffer();
}

async function main() {
  mkdirSync(outDir, { recursive: true });

  const browser = await playwright.chromium.launch();
  const page = await browser.newPage({
    viewport: { width: 1280, height: 800 },
    deviceScaleFactor: 1,
  });

  // Load the real page so the frames are rendered by the exact code we ship.
  await page.goto("file://" + join(root, "docs", "index.html"));
  await page.waitForFunction(
    () => typeof window.AgentPipeBanana4D?.renderTo === "function",
    null,
    { timeout: 10_000 },
  );

  const frames = [];
  for (let index = 0; index < FRAME_COUNT; index += 1) {
    const timeSeconds = Number((index * INTERVAL_SECONDS).toFixed(1));
    const dataUrl = await page.evaluate(
      ({ time, seed, width, height, dpr }) => {
        const canvas = document.createElement("canvas");
        canvas.width = Math.round(width * dpr);
        canvas.height = Math.round(height * dpr);
        window.AgentPipeBanana4D.renderTo(canvas, time, { seed, width, height, dpr });
        return canvas.toDataURL("image/png");
      },
      { time: timeSeconds, seed: SEED, width: CSS_WIDTH, height: CSS_HEIGHT, dpr: DPR },
    );

    let buffer = Buffer.from(dataUrl.replace(/^data:image\/png;base64,/, ""), "base64");
    if (optimize) {
      buffer = await optimizePng(buffer);
    }

    const dims = pngDimensions(buffer);
    if (dims.width !== CSS_WIDTH * DPR || dims.height !== CSS_HEIGHT * DPR) {
      throw new Error(
        `frame ${index + 1} rendered at ${dims.width}x${dims.height}, expected ${CSS_WIDTH * DPR}x${CSS_HEIGHT * DPR}`,
      );
    }

    const fileName = `frame-${String(index + 1).padStart(2, "0")}.png`;
    writeFileSync(join(outDir, fileName), buffer);
    frames.push({
      file: `assets/banana-frames/${fileName}`,
      timeSeconds,
      width: dims.width,
      height: dims.height,
      bytes: buffer.length,
      sha256: sha256(buffer),
    });
    console.log(
      `rendered ${fileName} @ t=${timeSeconds.toFixed(1)}s ${dims.width}x${dims.height} (${(buffer.length / 1024).toFixed(0)} KiB)`,
    );
  }

  await browser.close();

  const manifest = {
    description:
      "Deterministic pre-rendered frames of the 4D banana simulation, rendered by scripts/render-banana-frames.mjs using the same renderer as the live canvas. Embedded in the DOM at opacity 0 with alt text for screen reader users (issue #149).",
    renderer: "docs/banana4d.js :: window.AgentPipeBanana4D.renderTo",
    seed: SEED,
    cssDesignSize: { width: CSS_WIDTH, height: CSS_HEIGHT },
    devicePixelRatio: DPR,
    frameCount: FRAME_COUNT,
    intervalSeconds: INTERVAL_SECONDS,
    frames,
  };
  writeFileSync(join(outDir, "manifest.json"), JSON.stringify(manifest, null, 2) + "\n");
  console.log(`wrote manifest.json with ${frames.length} frames`);

  // Determinism self-check: re-render frame 1 and compare pixels byte-for-byte.
  const page2 = await (await playwright.chromium.launch()).newPage();
  await page2.goto("file://" + join(root, "docs", "index.html"));
  await page2.waitForFunction(() => typeof window.AgentPipeBanana4D?.renderTo === "function");
  const check = await page2.evaluate(
    ({ time, seed, width, height, dpr }) => {
      const canvas = document.createElement("canvas");
      canvas.width = Math.round(width * dpr);
      canvas.height = Math.round(height * dpr);
      window.AgentPipeBanana4D.renderTo(canvas, time, { seed, width, height, dpr });
      return canvas.toDataURL("image/png");
    },
    { time: 0, seed: SEED, width: CSS_WIDTH, height: CSS_HEIGHT, dpr: DPR },
  );
  let checkBuffer = Buffer.from(check.replace(/^data:image\/png;base64,/, ""), "base64");
  if (optimize) {
    checkBuffer = await optimizePng(checkBuffer);
  }
  if (sha256(checkBuffer) !== frames[0].sha256) {
    throw new Error("determinism self-check failed: re-rendered frame differs");
  }
  await page2.context().browser().close();
  console.log("determinism self-check passed");
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});
