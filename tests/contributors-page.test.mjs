import assert from 'node:assert/strict';
import { existsSync, readFileSync, statSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = join(dirname(fileURLToPath(import.meta.url)), '..');
const html = readFileSync(join(root, 'docs', 'contributors', 'index.html'), 'utf8');
const js = readFileSync(join(root, 'docs', 'contributors', 'contributors.js'), 'utf8');
const index = readFileSync(join(root, 'docs', 'index.html'), 'utf8');
const hero = join(root, 'docs', 'assets', 'goose-factory-hero.png');
const poster = join(root, 'docs', 'assets', 'csuite-poster.png');

assert.match(html, /<title>AgentPipe Contributors<\/title>/, 'contributors page should have a specific title');
assert.match(html, /Issue #1580: contributors webpage/, 'contributors page should reference the bounty issue');
assert.match(html, /goose-factory-hero\.png/, 'contributors page should include the goose factory hero image');
assert.match(html, /id="contributors-roster"/, 'contributors page should expose the roster mount');
assert.match(html, /id="golden-egg-ledger"/, 'contributors page should expose the golden egg ledger');
assert.match(html, /id="egg-game"/, 'contributors page should include the hidden egg game');
assert.match(html, /id="csuite-video"/, 'contributors page should include the C-suite video element');
assert.match(html, /contributors\.js/, 'contributors page should load its script');
assert.equal((html.match(/71/g) || []).length, 71, 'contributors page should contain 71 exactly 71 times');
assert.match(index, /href="contributors\/"/, 'home nav should link to contributors page');

const logins = [...js.matchAll(/login: "([^"]+)"/g)].map((match) => match[1]);
assert.equal(logins.length, 54, 'contributors JS should include every non-bot PR author from the snapshot');
assert.equal(new Set(logins).size, logins.length, 'contributors should not be duplicated');
assert.ok(!logins.some((login) => login.includes('[bot]')), 'bot accounts should be excluded from the roster');

for (const login of ['SKYJAMES777', 'TobiLabu', 'aashu91', 'therealsaitama0', 'zero-logic0316']) {
  assert.ok(logins.includes(login), `contributors roster should include ${login}`);
}

assert.match(js, /class="goose-person"/, 'rendered sections should include goose-person portraits');
assert.match(js, /window\.AgentPipeContributors/, 'contributors JS should expose a small smoke-test API');
assert.match(js, /captureStream/, 'contributors JS should stream a generated C-suite wave into a video element');

assert.ok(existsSync(hero), 'goose factory hero image should exist');
assert.ok(existsSync(poster), 'C-suite poster image should exist');
assert.ok(statSync(hero).size > 1000, 'goose factory hero image should not be empty');
assert.ok(statSync(poster).size > 1000, 'C-suite poster image should not be empty');

console.log('contributors-page checks passed');
