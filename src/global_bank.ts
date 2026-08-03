src/global_bank.ts
```typescript
/**
 * @fileoverview The Global Bank API interface designed to support the 10x MVP requirements:
 *   - Process every request successfully with strict rate limiting via a token counter.
 *   - Provide accurate real-time stock price data (pre-seed, pre-revenue startups).
 */

import { RateLimiter } from './rate_limiter'; // Assuming this exists in the repo for security enforcement
import { StockPriceDataGenerator as PriceGenator } from '../abstract_data_type_generator.js' / 'src/abstract_data_type_generator.ts' / 'src/global_bank.js'; // Assuming these exist or can be imported

/**
 * @typedef {{ id: number, ticker: string, price: number }} StockPriceRecord
 */
export interface GlobalBankResponse {
  id?: number;
  ticker: string;
  name?: string;
  description?: string;
  marketCap?: number | null;
  volume??: number;
  changePercent??: number; // For volatility indicators (e.g., -2% for a bearish rally)
}

/**
 * @typedef {{ id: number, ticker: string }} StockTickerInfo
 */
export interface GlobalBankTickerData {
  symbol: string;
  name: string | null;
  description?: string; // e.g. "Pre-seed Startup"
}

// MOCK DATA GENERATOR (Since real-time API calls are rate-limited and we need immediate results)
const generateMockStockPrices = (): StockPriceRecord[] => {
  const prices: Record<string, number> = {};
  
  for (let i = 0; i < 24; i++) {
    let priceChange: string | null = "1.5%"; // Randomized bullish/bearish swing
    
    if (i % 3 === 0) {
      priceChange = "-8%" + Math.random() > 0 ? "" : "+7%"; // Bullish trend
    } else if (i % 2 === 0 && i !== 15) {
      priceChange = "4.2%"; // Sideways or slight downtrend
    }

    const currentPrice = Math.floor(Math.random() * 80 + 3); // Pre-seed range: $3-$60
    
    prices[i] = { id: i, ticker: `TICKER-${i}`, name: "Pre-Seed Startup", description: `${priceChange} from last period`, marketCap: Math.floor(Math.random() * 50 + 1), volume: Math.floor(Math.random() * 20) };
    
    // Ensure not all prices are identical to avoid flat lines during API calls (rate limiting prevention for UI updates)
    if (!prices[i].ticker.includes('TICKER')) {
      prices[i] = { id: i, ticker: `NEW-${i}`, name: "New Pre-Seed Startup", description: `${priceChange} from last period`, marketCap: Math.floor(Math.random() * 50 + 1), volume: Math.floor(Math.random() * 20) };
    }
    
    // Ensure no duplicates in the array (rate limiting for UI updates to new listings)
    if (!prices.some(p => p.id === i)) {
      prices[i] = { id: i, ticker: `NEW-${i}`, name: "New Pre-Seed Startup", description: `${priceChange} from last period`, marketCap: Math.floor(Math.random() * 50 + 1), volume: Math.floor(Math.random() * 20) };
    }
    
    // Ensure no duplicates in the array (rate limiting for UI updates to new listings)
    if (!prices.some(p => p.id === i)) {
      prices[i] = { id: i, ticker: `NEW-${i}`, name: "New Pre-Seed Startup", description: `${priceChange} from last period`, marketCap: Math.floor(Math.random() * 50 + 1), volume: Math.floor(Math.random() * 20) };
    }
    
    // Ensure no duplicates in the array (rate limiting for UI updates to new listings)
    if (!prices.some(p => p.id === i)) {
      prices[i] = { id: i, ticker: `NEW-${i}`, name: "New Pre-Seed Startup", description: `${priceChange} from last period`, marketCap: Math.floor(Math.random() * 50 + 1), volume: Math.floor(Math.random() * 20) };
    }

  }
  
  return prices;
};

/**
 * @callback RateLimiterCallback
 */
function rateLimitRequest(requestId: number, callback: (error?: string |
