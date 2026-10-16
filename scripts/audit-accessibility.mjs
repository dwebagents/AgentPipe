#!/usr/bin/env node
/**
 * Automated accessibility audit for the AgentPipe docs site (issue #149).
 *
 * Runs axe-core against every page under multiple scenarios:
 *   - desktop viewport (1280x800)
 *   - mobile viewport (375x667, DPR 3)
 *   - prefers-reduced-motion: reduce
 *   - after activating the motion toggle (keyboard only)
 *
 * It also performs checks axe cannot express:
 *   - every image decodes (no broken sources)
 *   - the opacity-0 pre-rendered frames stay in the accessibility tree
 *   - the pause control is keyboard operable and its aria-pressed + live
 *     status update correctly
 *
 * Usage:
 *   export NODE_PATH="$(npm root -g)"   # where playwright lives
 *   node scripts/audit-accessibility.mjs
 *
 * axe-core is loaded from the jsDelivr CDN (cached to a temp file when the
 * network is unavailable at first attempt).
 */

import { createRequire } from "node:module";
import { createServer } from "node:http";
import { readFile, writeFile, unlink } from "node:fs/promises";
import { dirname, join, extname } from "node:path";
import { fileURLToPath } from "node:url";
import os from "node:os";

const require = createRequire(import.meta.url);
let playwright;
try {
  playwright = require("playwright");
} catch {
  console.error('playwright is required. Run with: export NODE_PATH="$(npm root -g)"');
  process.exit(1);
}

const root = join(dirname(fileURLToPath(import.meta.url)), "..");
const docsDir = join(root, "docs");
const AXE_URL = "https://cdn.jsdelivr.net/npm/axe-core@4.10.2/axe.min.js";
const AXE_CACHE = join(os.tmpdir(), "axe-core-4.10.2.min.js");

const MIME = { ".html": "text/html", ".css": "text/css", ".js": "text/javascript", ".svg": "image/svg+xml", ".png": "image/png", ".json": "application/json" };

async function loadAxeSource() {
  try {
    const res = await fetch(AXE_URL);
    if (res.ok) {
      const source = await res.text();
      await writeFile(AXE_CACHE, source, "utf8");
      return source;
    }
  } catch {
    // fall through to cache
  }
  return readFile(AXE_CACHE, "utf8");
}

function startServer() {
  return new Promise((resolve) => {
    const server = createServer(async (req, res) => {
      const urlPath = decodeURIComponent(new URL(req.url, "http://localhost").pathname);
      let filePath = join(docsDir, urlPath === "/" ? "index.html" : urlPath);
      try {
        const body = await readFile(filePath);
        res.writeHead(200, { "content-type": MIME[extname(filePath)] || "application/octet-stream" });
        res.end(body);
      } catch {
        res.writeHead(404);
        res.end("not found");
      }
    });
    server.listen(0, "127.0.0.1", () => resolve(server));
  });
}

async function runAxe(page, label) {
  const results = await page.evaluate(() =>
    window.axe.run(document, {
      resultTypes: ["violations"],
      runOnly: ["wcag2a", "wcag2aa", "wcag21a", "wcag21aa", "wcag22aa", "best-practice"],
    }),
  );
  const violations = results.violations.map((v) => ({
    id: v.id,
    impact: v.impact,
    help: v.help,
    nodes: v.nodes.length,
  }));
  return { label, violations, passes: results.passes.length, incomplete: results.incomplete.length };
}

async function inspectBeyondAxe(page) {
  return page.evaluate(() => {
    const imgs = [...document.querySelectorAll("img")];
    const broken = imgs.filter((img) => !(img.complete && img.naturalWidth > 0)).map((img) => img.getAttribute("src"));
    const framesContainer = document.getElementById("banana-prerendered-frames");
    const opacity = framesContainer ? getComputedStyle(framesContainer).opacity : null;
    const frameImgs = imgs.filter((img) => img.closest("#banana-prerendered-frames"));
    return {
      totalImages: imgs.length,
      brokenImages: broken,
      framesContainerOpacity: opacity,
      frameImageCount: frameImgs.length,
    };
  });
}

async function main() {
  const [axeSource, server] = await Promise.all([loadAxeSource(), startServer()]);
  const { port } = server.address();
  const base = `http://127.0.0.1:${port}`;
  const browser = await playwright.chromium.launch();
  const report = [];

  const scenarios = [
    { name: "desktop", viewport: { width: 1280, height: 800 }, deviceScaleFactor: 1 },
    { name: "mobile", viewport: { width: 375, height: 667 }, deviceScaleFactor: 3, isMobile: true, hasTouch: true },
    {
      name: "reduced-motion",
      viewport: { width: 1280, height: 800 },
      deviceScaleFactor: 1,
      reducedMotion: "reduce",
    },
  ];

  for (const path of ["/index.html", "/butter.html"]) {
    for (const scenario of scenarios) {
      const context = await browser.newContext(scenario);
      const page = await context.newPage();
      await page.goto(base + path, { waitUntil: "networkidle" });
      await page.addScriptTag({ content: axeSource });

      const label = `${path} :: ${scenario.name}`;
      report.push(await runAxe(page, label));

      if (path === "/index.html") {
        const beyond = await inspectBeyondAxe(page);
        report.push({ label: `${label} beyond-axe`, ...beyond, violations: [] });

        // Initial motion state must respect prefers-reduced-motion before any
        // interaction happens.
        const initialMotionState = await page.evaluate(() => ({
          pressed: document.getElementById("banana-motion-toggle")?.getAttribute("aria-pressed"),
          status: document.getElementById("banana-motion-status")?.textContent,
        }));
        report.push({
          label: `${label} initial-motion-state`,
          violations: [],
          ...initialMotionState,
          reducedMotionEmulated: scenario.reducedMotion === "reduce",
        });

        // Keyboard: skip link first, then walk tab stops until the toggle.
        await page.keyboard.press("Tab");
        const firstFocus = await page.evaluate(() => document.activeElement?.className || "");
        let tabStops = 1;
        let reachedToggle = false;
        for (let i = 0; i < 14; i += 1) {
          const activeId = await page.evaluate(() => document.activeElement?.id || "");
          if (activeId === "banana-motion-toggle") {
            reachedToggle = true;
            break;
          }
          await page.keyboard.press("Tab");
          tabStops += 1;
        }
        report.push({
          label: `${label} keyboard`,
          violations: [],
          firstFocusIsSkipLink: firstFocus.includes("skip-link"),
          toggleReachedByTab: reachedToggle,
          tabStopsToToggle: reachedToggle ? tabStops : null,
        });

        await page.keyboard.press("Enter");
        const toggleState = await page.evaluate(() => ({
          pressed: document.getElementById("banana-motion-toggle")?.getAttribute("aria-pressed"),
          status: document.getElementById("banana-motion-status")?.textContent,
          buttonText: document.getElementById("banana-motion-toggle")?.textContent,
        }));
        report.push({
          label: `${label} motion-toggle-keyboard`,
          violations: [],
          ...toggleState,
        });
      }

      await context.close();
    }
  }

  // Accessibility-tree evidence: the opacity-0 frames must be exposed.
  const context = await browser.newContext({ viewport: { width: 1280, height: 800 } });
  const page = await context.newPage();
  await page.goto(base + "/index.html", { waitUntil: "networkidle" });
  // Wait until every image (including lazy-loaded frames) is fully decoded so
  // the snapshot reflects what a screen reader sees on a settled page.
  await page.waitForFunction(
    () => [...document.images].every((img) => img.complete && img.naturalWidth > 0),
    null,
    { timeout: 15_000 },
  );
  const snapshot = await page.locator("body").ariaSnapshot();
  // YAML quotes the role name when the alt text contains a colon:
  // `- img "At 0.0 seconds ..."` vs `- 'img "At 0.5 seconds ..."'`.
  const imageRoleLines = (snapshot.match(/- '?img "/g) || []).length;
  // aria-roledescription is not echoed by ariaSnapshot; verify the roles and
  // position metadata from the DOM instead, and count exposed images in the
  // accessibility tree snapshot itself.
  const domCheck = await page.evaluate(() => {
    const figures = [...document.querySelectorAll("#banana-prerendered-frames figure")];
    return {
      figureCount: figures.length,
      roledescriptions: figures.map((f) => f.getAttribute("aria-roledescription")),
      allWithCaptions: figures.every((f) => f.querySelector("figcaption[id]")),
      imgsDescribedByCaptions: figures.every((f) => {
        const img = f.querySelector("img");
        const caption = f.querySelector("figcaption[id]");
        return img && caption && (img.getAttribute("aria-describedby") || "").includes(caption.id);
      }),
    };
  });
  const altSamples = [...snapshot.matchAll(/At ([\d.]+) seconds[^"\n]{0,60}/g)].slice(0, 3).map((m) => m[0]);
  report.push({
    label: "accessibility-tree",
    violations: [],
    exposedImageRoles: imageRoleLines,
    ...domCheck,
    sampleAltAnnouncements: altSamples,
  });
  await context.close();

  await browser.close();
  server.close();

  let failures = 0;
  for (const entry of report) {
    const bad = (entry.violations || []).filter((v) => v.impact !== null);
    if (bad.length) failures += bad.length;
    if ((entry.violations || []).length) {
      console.log(`\n${entry.label}`);
      for (const v of entry.violations) console.log(`  ${v.impact || "?"} | ${v.id} | ${v.help} | nodes: ${v.nodes}`);
    } else if (!("sampleAltAnnouncements" in entry)) {
      console.log(`${entry.label}: no violations`);
    }
  }

  console.log("\n--- beyond-axe summary ---");
  for (const entry of report) {
    if ("exposedImageRoles" in entry) {
      // 12 pre-rendered frames + 1 canvas with role="img" must all be exposed.
      const expected = 13;
      const ok = entry.exposedImageRoles === expected && entry.figureCount === 12 && entry.allWithCaptions && entry.imgsDescribedByCaptions;
      if (!ok) failures += 1;
      console.log(
        `accessibility tree: ${entry.exposedImageRoles}/${expected} exposed img roles (12 frames + canvas); figures=${entry.figureCount} allCaptions=${entry.allWithCaptions} imgDescribedByCaption=${entry.imgsDescribedByCaptions} -> ${ok ? "OK" : "FAIL"}`,
      );
      console.log(`  frame roledescriptions: ${entry.roledescriptions[0]} ... ${entry.roledescriptions[11]}`);
      entry.sampleAltAnnouncements.forEach((s) => console.log(`  sample announcement: "${s}..."`));
    }
    if ("framesContainerOpacity" in entry) {
      const ok = entry.brokenImages.length === 0 && entry.frameImageCount === 12 && Number(entry.framesContainerOpacity) === 0;
      if (!ok) failures += 1;
      console.log(
        `${entry.label}: images=${entry.totalImages} broken=${entry.brokenImages.length} frameImgs=${entry.frameImageCount} containerOpacity=${entry.framesContainerOpacity} -> ${ok ? "OK" : "FAIL"}`,
      );
    }
    if ("firstFocusIsSkipLink" in entry) {
      const ok = entry.firstFocusIsSkipLink && entry.toggleReachedByTab;
      if (!ok) failures += 1;
      console.log(
        `${entry.label}: skip-link-first=${entry.firstFocusIsSkipLink} toggleReachedByTab=${entry.toggleReachedByTab} tabStops=${entry.tabStopsToToggle} -> ${ok ? "OK" : "FAIL"}`,
      );
    }
    if ("reducedMotionEmulated" in entry) {
      const expectPaused = entry.reducedMotionEmulated;
      const ok = expectPaused ? entry.pressed === "true" && entry.status.length > 0 : entry.pressed === "false";
      if (!ok) failures += 1;
      console.log(
        `${entry.label}: aria-pressed=${entry.pressed} status="${entry.status}" (reducedMotion=${entry.reducedMotionEmulated}) -> ${ok ? "OK" : "FAIL"}`,
      );
    }
    if ("buttonText" in entry) {
      const ok = entry.buttonText.length > 0 && entry.status.length > 0;
      if (!ok) failures += 1;
      console.log(`${entry.label}: after Enter -> aria-pressed=${entry.pressed} button="${entry.buttonText}" status="${entry.status}" -> ${ok ? "OK" : "FAIL"}`);
    }
  }

  const violationsTotal = report.reduce((n, r) => n + (r.violations ? r.violations.filter((v) => v.impact).length : 0), 0);
  console.log(`\nTOTAL blocking violations: ${violationsTotal}`);
  await unlink(AXE_CACHE).catch(() => {});
  process.exit(failures === 0 ? 0 : 1);
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});
