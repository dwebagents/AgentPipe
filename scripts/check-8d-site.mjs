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
  "banana8d.js",
]) {
  if (!html.includes(token)) {
    throw new Error(`docs/index.html is missing ${token}`);
  }
}

for (const token of [
  ".lab8d-band",
  ".chess8d-board",
  ".chess8d-cell.active",
]) {
  if (!css.includes(token)) {
    throw new Error(`docs/styles.css is missing ${token}`);
  }
}

for (const token of [
  "function rotate8d",
  "function project8d",
  "window.AgentPipe8D",
]) {
  if (!js.includes(token)) {
    throw new Error(`docs/banana8d.js is missing ${token}`);
  }
}

console.log("AgentPipe 8D site checks passed.");
