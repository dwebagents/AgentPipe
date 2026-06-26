import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {resolve} from 'node:path';

const scriptPath = resolve('scripts/mascot-pattern.pl');
const source = readFileSync(scriptPath, 'utf8');

assert.match(source, /^#!.*perl/m, 'script should be directly runnable with Perl');
assert.match(source, /use strict;/, 'script should enable strict mode');
assert.match(source, /use warnings;/, 'script should enable warnings');
assert.match(source, /Getopt::Long/, 'script should use core option parsing');

for (const option of ['banana', 'goose', 'goblin', 'yarn-weight', 'craft', 'name', 'help']) {
  assert.match(source, new RegExp(`'${option}`), `script should accept --${option}`);
}

for (const section of ['Materials', 'Gauge and sizing', 'Pattern instructions', 'Assembly']) {
  assert.match(source, new RegExp(`## ${section}`), `output should include a ${section} section`);
}

assert.match(source, /my %yarn_weights = \(/, 'script should scale output by yarn weight');
assert.match(source, /sub ratio_percentages/, 'script should calculate motif percentages');
assert.match(source, /sub build_row_plan/, 'script should generate row-by-row instructions');
assert.match(source, /crochet\|knit/, 'script should document both supported craft modes');
assert.doesNotMatch(source, /https?:\/\//i, 'script should not depend on remote services');
