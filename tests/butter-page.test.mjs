import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = join(dirname(fileURLToPath(import.meta.url)), '..');
const html = readFileSync(join(root, 'docs', 'butter.html'), 'utf8');
const js = readFileSync(join(root, 'docs', 'butter.js'), 'utf8');
const index = readFileSync(join(root, 'docs', 'index.html'), 'utf8');

assert.match(html, /<title>AgentPipe Butter Mode<\/title>/, 'butter page should have a specific title');
assert.match(html, /Issue #1878: butter/, 'butter page should reference the bounty issue');
assert.match(html, /id="spread-input"/, 'butter page should expose a spread range control');
assert.match(html, /id="butter-state"/, 'butter page should expose state selection');
assert.match(html, /id="butter-button"/, 'butter page should expose an apply button');
assert.match(html, /id="butter-spread"/, 'butter page should expose a visual meter');
assert.match(html, /id="butter-log"/, 'butter page should expose live output');
assert.match(html, /butter\.js/, 'butter page should load its script');
assert.match(html, /spread|churn|melt|clarify/, 'butter page should include the butter lifecycle states');
assert.match(index, /href="butter\.html"/, 'home nav should link to butter page');

for (const state of ['spread', 'churn', 'melt', 'clarify']) {
  assert.match(js, new RegExp(`${state}:`), `butter JS should define copy for ${state}`);
}
assert.match(js, /window\.AgentPipeButter/, 'butter JS should expose a small smoke-test API');
assert.match(js, /dataset\.coverage/, 'butter JS should store rendered coverage for smoke testing');

console.log('butter-page checks passed');
