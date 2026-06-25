import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {resolve} from 'node:path';

const pagePath = resolve('docs/index.html');
const html = readFileSync(pagePath, 'utf8');

assert.match(html, /<title>\s*AgentPipe\s*<\/title>/i, 'page title should be AgentPipe');
assert.match(html, /AgentPipe turns/i, 'page should explain what the project does');
assert.match(html, /github\.com\/dwebagents\/AgentPipe\/archive\/refs\/heads\/main\.zip/i, 'page should link a downloadable project archive');
assert.match(html, /id="banana-hypercanvas"/i, 'page should expose the banana render canvas');
assert.match(html, /BANANA_SEED\s*=\s*112200/i, 'banana render should use a fixed deterministic seed');
assert.match(html, /function\s+project4Dto2D/i, 'banana render should project 4D points into the viewport');
assert.match(html, /function\s+generateBananaMesh/i, 'banana render should generate banana geometry client-side');
assert.match(html, /function\s+renderBananaFrame/i, 'banana render should render frames client-side');
assert.match(html, /--banana-yellow/i, 'page should define a banana-yellow theme token');
assert.doesNotMatch(html, /<script[^>]+src=["']https?:\/\//i, 'website should not depend on remote script CDNs');
