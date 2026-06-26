import { readFileSync, statSync } from "node:fs";
import { join } from "node:path";

const root = new URL("..", import.meta.url).pathname;

const requiredFiles = [
  "docs/index.html",
  "docs/assets/site.css",
  "docs/assets/banana4d.js",
  ".github/workflows/pages.yml",
];

for (const file of requiredFiles) {
  const fullPath = join(root, file);
  const stats = statSync(fullPath);
  if (!stats.isFile() || stats.size === 0) {
    throw new Error(`${file} must exist and be non-empty`);
  }
}

const html = readFileSync(join(root, "docs/index.html"), "utf8");
const css = readFileSync(join(root, "docs/assets/site.css"), "utf8");
const js = readFileSync(join(root, "docs/assets/banana4d.js"), "utf8");

const requiredHtml = [
  "AgentPipe",
  "Download project",
  "banana-canvas",
  "Projected 4D banana",
  "https://github.com/dwebagents/AgentPipe/archive/refs/heads/main.zip",
];

for (const token of requiredHtml) {
  if (!html.includes(token)) {
    throw new Error(`docs/index.html is missing ${token}`);
  }
}

const requiredJs = ["SEED", "bananaPoint", "rotate4d", "project4Dto2D"];
for (const token of requiredJs) {
  if (!js.includes(token)) {
    throw new Error(`banana4d.js is missing ${token}`);
  }
}

const requiredCss = ["--yellow-500", ".banana-stage", "@media"];
for (const token of requiredCss) {
  if (!css.includes(token)) {
    throw new Error(`site.css is missing ${token}`);
  }
}

console.log("AgentPipe website checks passed.");
