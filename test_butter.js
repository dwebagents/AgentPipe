const fs = require('fs');
const path = require('path');

const docsDir = path.join(__dirname, 'docs');
const indexPath = path.join(docsDir, 'index.html');
const butterHtmlPath = path.join(docsDir, 'butter.html');
const butterJsPath = path.join(docsDir, 'butter.js');

let failed = false;

function assert(condition, message) {
  if (!condition) {
    console.error('FAIL:', message);
    failed = true;
  } else {
    console.log('PASS:', message);
  }
}

assert(fs.existsSync(indexPath), 'docs/index.html exists');

const indexHtml = fs.readFileSync(indexPath, 'utf8');
assert(indexHtml.includes('butter.html'), 'docs/index.html links to butter.html');

assert(fs.existsSync(butterHtmlPath), 'docs/butter.html exists');
const butterHtml = fs.readFileSync(butterHtmlPath, 'utf8');
assert(butterHtml.includes('Butter Mode'), 'butter.html contains "Butter Mode" title');
assert(butterHtml.includes('<script src="butter.js">'), 'butter.html includes butter.js script');
assert(butterHtml.includes('id="coverage"'), 'butter.html has coverage input');
assert(butterHtml.includes('id="state"'), 'butter.html has state select');
assert(butterHtml.includes('id="liveLog"'), 'butter.html has liveLog element');

assert(fs.existsSync(butterJsPath), 'docs/butter.js exists');
const butterJs = fs.readFileSync(butterJsPath, 'utf8');
assert(butterJs.includes('window.AgentPipeButter'), 'butter.js exposes window.AgentPipeButter');
assert(butterJs.includes("'spread'"), 'butter.js supports spread state');
assert(butterJs.includes("'churn'"), 'butter.js supports churn state');
assert(butterJs.includes("'melt'"), 'butter.js supports melt state');
assert(butterJs.includes("'clarify'"), 'butter.js supports clarify state');
assert(butterJs.includes('71'), 'butter.js has default 71 coverage');

if (failed) {
  console.error('\nButter mode static acceptance checks failed.');
  process.exit(1);
}
console.log('\nAll butter mode checks passed.');
