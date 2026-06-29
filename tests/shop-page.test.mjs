import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';

const root = join(dirname(fileURLToPath(import.meta.url)), '..');
const html = readFileSync(join(root, 'docs', 'shop.html'), 'utf8');
const js = readFileSync(join(root, 'docs', 'shop.js'), 'utf8');
const logo = readFileSync(join(root, 'docs', 'logo.svg'), 'utf8');

assert.match(html, /<title>AgentPipe Shop<\/title>/, 'shop page should have a page-specific title');
assert.match(html, /id="product-grid"/, 'shop page should expose a product grid');
assert.match(html, /id="tag-filter"/, 'shop page should include tag filtering');
assert.match(html, /id="min-price"/, 'shop page should include min price filtering');
assert.match(html, /id="max-price"/, 'shop page should include max price filtering');
assert.match(html, /id="sort-products"/, 'shop page should include sorting controls');
assert.match(html, /id="locale-select"/, 'shop page should include locale selector');
assert.match(html, /id="currency-select"/, 'shop page should include currency selector');
assert.match(html, /id="cart-items"/, 'shop page should include a shopping cart');
assert.match(html, /id="coupon-code"/, 'shop page should include coupon support');
assert.match(html, /id="checkout-mode"/, 'shop page should include guest/auth checkout mode');
assert.match(html, /id="payment-method"/, 'shop page should include payment method selection');
assert.match(html, /id="shop-machine"/, 'shop page should include the cart mechanism animation target');
assert.match(html, /shop\.js/, 'shop page should load shop.js');
assert.match(logo, /<svg[\s>]/, 'docs logo should be available for GitHub Pages deployment');
assert.match(html, /cheap-mass-market|premium-luxury/, 'shop page should include dynamic theme hooks');

const productMatches = [...js.matchAll(/id:\s*"product-(\d+)"/g)];
assert.equal(productMatches.length, 71, 'shop should define exactly 71 products');
assert.equal(new Set(productMatches.map((m) => m[1])).size, 71, 'product ids should be unique');
assert.match(js, /skyjames777 commemorative broach/i, 'shop should include the commemorative product');
assert.match(js, /VALUED/, 'shop should implement VALUED coupon');
assert.match(js, /\b71\b/, 'shop should implement 71 coupon');
assert.match(js, /Goose Pay|FTX|Apple Pay|Google Pay|AliPay|Samsung Pay|PayPal|Cash App/, 'shop should expose parody payment methods');
assert.match(js, /detectCustomerTier|applyLocale|renderProducts|addToCart|applyCoupon|checkout/, 'shop JS should expose the required interaction functions');

console.log('shop-page checks passed');
