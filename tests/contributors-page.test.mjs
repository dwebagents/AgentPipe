import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = join(dirname(fileURLToPath(import.meta.url)), '..');
const html = readFileSync(join(root, 'docs', 'contributors', 'index.html'), 'utf8');
const index = readFileSync(join(root, 'docs', 'index.html'), 'utf8');

// 1. Page title and identity
assert.match(html, /<title>AgentPipe Contributors.*<\/title>/, 'Contributors page should have a clear title');

// 2. Hero with corporate-friendly goose people working in factory
assert.match(html, /factory-svg/, 'Hero must contain goose factory illustration');
assert.match(html, /Precision Pipe Fabrication Facility/, 'Factory must describe assembly facility');

// 3. Every non-C-Suite PR contributor has a dedicated card
const expectedContributors = [
  'Meart67', 'kveita', 'arsen-ask-lx', 'OreoMuncher45', '0xalydev',
  'Silverbullets1', 'Martob13', 'jeanclawd-agent', '0xhermes-28', 'jamboriu',
  'Ariyan-Pro', 'waterWang', 'gianmarcozap', 'laurentketterle-hub', 'q514168795',
  'EnderChest-YT', 'lushan888', 'Ektisad25', 'Adraca', 'yh-liao-07'
];

for (const user of expectedContributors) {
  assert.match(html, new RegExp(`contributor-${user}`), `Page must contain dedicated section for @${user}`);
  assert.match(html, new RegExp(`https://github.com/${user}`), `Page must link to GitHub profile for @${user}`);
}

// 4. Facts about agents
assert.match(html, /Birthplace:/, 'Cards must include agent birthplace fact');
assert.match(html, /Latest Prompt:/, 'Cards must include agent latest prompt fact');

// 5. Every portrait is a goose person
assert.match(html, /goose-portrait-svg/, 'Every portrait must be a vector goose person');

// 6. Decorated with golden eggs
assert.match(html, /🥚/, 'Page must feature golden eggs decoration');

// 7. Easter egg game
assert.match(html, /The Great Golden Egg Hunt/, 'Page must contain interactive egg hunt game');
assert.match(html, /gameBoard/, 'Page must contain game board');

// 8. Number 71 appears exactly 71 times
const matches71 = (html.match(/71/g) || []).length;
assert.equal(matches71, 71, `The number 71 must appear exactly 71 times (found ${matches71})`);

// 9. C-Suite contact info & waving video
assert.match(html, /C-Suite Executive Governance/, 'Footer must list C-Suite governance');
assert.match(html, /c-suite@agentpipe.com/, 'Footer must provide C-Suite contact');
assert.match(html, /<video.*autoplay.*loop/s, 'Footer must feature waving video element');

// 10. Nav link in main docs/index.html
assert.match(index, /href="contributors\/"/, 'Main docs/index.html should link to contributors');

console.log('All contributors-page checks passed successfully! 🪿🥚');
