import { readFileSync, statSync } from "node:fs";

const requiredFiles = [
  "docs/index.html",
  "docs/styles.css",
  "docs/banana8d.js",
];

for (const file of requiredFiles) {
  const stats = statSync(file);
  if (!stats.isFile() || stats.size === 0) {
    throw new Error(`${file} must exist and be non-empty`);
  }
}

const html = readFileSync("docs/index.html", "utf8");
const css = readFileSync("docs/styles.css", "utf8");
const js = readFileSync("docs/banana8d.js", "utf8");

for (const token of [
  "8D Lab",
  "audio8d-toggle",
  "chess8d-board",
  "chess8d-roster",
  "banana8d.js",
]) {
  if (!html.includes(token)) {
    throw new Error(`docs/index.html is missing ${token}`);
  }
}

for (const token of [
  ".lab8d-band",
  ".chess8d-board",
  ".chess8d-roster",
  ".chess8d-roster-player",
  ".chess8d-cell.active",
]) {
  if (!css.includes(token)) {
    throw new Error(`docs/styles.css is missing ${token}`);
  }
}

for (const token of [
  "function rotate8d",
  "function project8d",
  "function buildBananaMusicBuffer",
  "function create8DChessPieces",
  "function chessVector",
  "function renderChessRoster",
  "TOTAL_CHESS_PIECES = PLAYER_COUNT * PIECES_PER_PLAYER",
  "musicSource = audioContext.createBufferSource()",
  "musicSource.buffer = musicBuffer",
  "pieces.length !== TOTAL_CHESS_PIECES",
  "window.AgentPipe8D",
]) {
  if (!js.includes(token)) {
    throw new Error(`docs/banana8d.js is missing ${token}`);
  }
}

if (js.includes("createOscillator")) {
  throw new Error("docs/banana8d.js should play back music instead of using a plain oscillator");
}

if (!js.includes("const PLAYER_COUNT = 8") || !js.includes("const PIECES_PER_PLAYER = 16")) {
  throw new Error("docs/banana8d.js must model eight players with 16 pieces each");
}

const playerLoop = js.match(/playerIndex < PLAYER_COUNT/g) || [];
if (playerLoop.length < 1 || !js.includes("pieces.length")) {
  throw new Error("docs/banana8d.js must build and expose all 128 projected 8D chess pieces");
}

console.log("AgentPipe 8D site checks passed.");
