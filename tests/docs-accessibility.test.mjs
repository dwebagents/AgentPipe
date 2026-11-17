import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import { existsSync, readFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = join(dirname(fileURLToPath(import.meta.url)), '..');
const read = (...parts) => readFileSync(join(root, ...parts), 'utf8');

const index = read('docs', 'index.html');
const butter = read('docs', 'butter.html');
const css = read('docs', 'styles.css');
const bananaJs = read('docs', 'banana4d.js');

const FRAME_COUNT = 12;
const FRAME_WIDTH = 1520;
const FRAME_HEIGHT = 1120;

// ---------------------------------------------------------------------------
// 1. Pre-rendered frames: real PNGs at full resolution, matching the manifest.
// ---------------------------------------------------------------------------
const manifest = JSON.parse(read('docs', 'assets', 'banana-frames', 'manifest.json'));
assert.equal(manifest.frameCount, FRAME_COUNT, 'manifest should list 12 frames');
assert.equal(manifest.seed, 314159, 'manifest should pin the simulation seed');
assert.deepEqual(
  manifest.cssDesignSize,
  { width: 760, height: 560 },
  'manifest should record the canvas CSS design size',
);
assert.equal(manifest.devicePixelRatio, 2, 'manifest should record devicePixelRatio 2');

function pngDimensions(buffer) {
  const signature = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);
  assert.ok(buffer.subarray(0, 8).equals(signature), 'frame must be a real PNG');
  return { width: buffer.readUInt32BE(16), height: buffer.readUInt32BE(20) };
}

manifest.frames.forEach((frame, i) => {
  const file = join(root, 'docs', frame.file);
  assert.ok(existsSync(file), `frame ${i + 1} should exist on disk: ${frame.file}`);
  const buffer = readFileSync(file);
  const dims = pngDimensions(buffer);
  assert.equal(
    dims.width,
    FRAME_WIDTH,
    `frame ${i + 1} should be full resolution width ${FRAME_WIDTH}`,
  );
  assert.equal(
    dims.height,
    FRAME_HEIGHT,
    `frame ${i + 1} should be full resolution height ${FRAME_HEIGHT}`,
  );
  const hash = createHash('sha256').update(buffer).digest('hex');
  assert.equal(
    hash,
    frame.sha256,
    `frame ${i + 1} bytes must match the manifest checksum (deterministic render)`,
  );
  assert.equal(frame.width, FRAME_WIDTH, `manifest width for frame ${i + 1}`);
  assert.equal(frame.height, FRAME_HEIGHT, `manifest height for frame ${i + 1}`);
  assert.equal(
    frame.timeSeconds,
    Number((i * 0.5).toFixed(1)),
    `frame ${i + 1} should be captured at ${(i * 0.5).toFixed(1)}s`,
  );
});

// ---------------------------------------------------------------------------
// 2. DOM embedding: every frame present with alt text, aria attributes,
//    width/height, at opacity 0 (screen-reader only layer).
// ---------------------------------------------------------------------------
for (let i = 1; i <= FRAME_COUNT; i++) {
  const nn = String(i).padStart(2, '0');
  const imgPattern = new RegExp(
    `<img\\s+src="assets/banana-frames/frame-${nn}\\.png"\\s+width="1520"\\s+height="1120"`,
  );
  assert.match(index, imgPattern, `frame ${i} img should reference its PNG at full resolution`);
  const figureBlock = index.slice(
    index.indexOf(`aria-roledescription="pre-rendered frame ${i} of 12"`),
  );
  assert.ok(figureBlock.length > 0, `frame ${i} figure should exist`);
  const figureHtml = figureBlock.slice(0, figureBlock.indexOf('</figure>'));
  assert.match(figureHtml, /alt="[ FatA][^"]{60,}"/, `frame ${i} img needs substantial alt text`);
  assert.match(figureHtml, /aria-describedby="banana-frame-\d+-caption"/, `frame ${i} img should be described by its caption`);
  assert.match(figureHtml, new RegExp(`id="banana-frame-${nn}-caption"`), `frame ${i} caption should exist`);
}

assert.match(
  index,
  /id="banana-prerendered-frames"[^>]*aria-label="Twelve pre-rendered full resolution PNG frames/,
  'frames container should carry a descriptive aria-label',
);
assert.match(
  index,
  /class="banana-prerendered-frames"/,
  'frames container should use the screen-reader-only class',
);
const framesCss = css.slice(css.indexOf('.banana-prerendered-frames {'));
const framesCssBlock = framesCss.slice(0, framesCss.indexOf('}'));
assert.match(
  framesCssBlock,
  /opacity:\s*0/,
  'frames container must be hidden with opacity 0 (kept in the accessibility tree)',
);
assert.match(framesCssBlock, /pointer-events:\s*none/, 'frames container must not intercept input');

// ---------------------------------------------------------------------------
// 3. Canvas text equivalent + motion controls.
// ---------------------------------------------------------------------------
assert.match(index, /<canvas[^>]*role="img"/, 'canvas should expose role="img"');
assert.match(index, /aria-labelledby="banana-visual-title"/, 'canvas should be labelled');
assert.match(index, /aria-describedby="banana-visual-description banana-frames-intro"/, 'canvas should point to its long description');
assert.match(index, />[^<]*Animated 4D banana simulation[^<]*</, 'canvas should contain fallback text');
assert.match(index, /id="banana-motion-toggle"/, 'motion toggle button should exist');
assert.match(index, /id="banana-motion-status"[^>]*role="status"/, 'motion status live region should exist');
assert.match(bananaJs, /aria-pressed/, 'toggle should track aria-pressed state');
assert.match(bananaJs, /prefers-reduced-motion/, 'simulation should honour reduced motion');
assert.match(bananaJs, /AgentPipeBanana4D/, 'deterministic render API should be exposed');

// ---------------------------------------------------------------------------
// 4. Reproducibility tooling + logo fix.
// ---------------------------------------------------------------------------
assert.ok(
  existsSync(join(root, 'scripts', 'render-banana-frames.mjs')),
  'pre-render script should be committed so frames are reproducible',
);
assert.ok(existsSync(join(root, 'docs', 'logo.svg')), 'docs should ship its own logo.svg');
assert.doesNotMatch(butter, /src="\.\.\/logo\.svg"/, 'butter page should not escape the docs root for the logo');
assert.match(butter, /src="logo\.svg"/, 'butter page should reference the local logo');
assert.match(butter, /prefers-reduced-motion/, 'butter orb should stop wobbling under reduced motion');

console.log('docs accessibility checks passed: 12 full-res frames, manifest checksums, DOM embedding, motion controls, logo fix');
