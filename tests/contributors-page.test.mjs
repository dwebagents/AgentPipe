import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = join(dirname(fileURLToPath(import.meta.url)), '..');
const html = readFileSync(join(root, 'docs', 'contributors.html'), 'utf8');
const js = readFileSync(join(root, 'docs', 'contributors.js'), 'utf8');
const index = readFileSync(join(root, 'docs', 'index.html'), 'utf8');

assert.match(html, /contributors\.html/, 'contributors page exists');
assert.match(html, /contributor-grid/, 'contributors grid container');
assert.match(html, /golden-egg/, 'golden eggs decoration');
assert.match(html, /C-Suite Contact/, 'csuite footer');
assert.match(html, /contributors\.js/, 'loads contributors script');
assert.match(js, /injectSeventyOnes/, 'seventy-one ritual');
assert.match(js, /AgentPipeContributors/, 'smoke test API');
assert.match(index, /contributors\.html/, 'home links to contributors');

console.log('contributors-page checks passed');
