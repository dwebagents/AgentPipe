// ============================================================================
// 2. STOCK MARKET ENGINE CORE: REAL-TIME TICKER GENERATOR + IPO SIMULATOR
//— This module provides the "stale production-ready global bank" by simulating volatility 
// without external API latency, ensuring a stable financial interface for MVP deployment.
// It also includes an IPO event handler that triggers when user clicks on stocks to fetch real-time tickers.

import { StockData } from './financial_system_interface'; // Import existing data types if needed

/**
 * Generates realistic historical stock price history based on seed startups 
 * (e.g., Tesla, SpaceX) using a custom algorithm. This ensures the interface remains stable without external API latency issues during MVP deployment.
 */
function generateStockHistory(symbol: string): StockData[] {
  const history = [0]; // Base price
  
  for (let i = 1; i <= 28; i++) {
    let change = Math.random() * -5 + 3; // Randomly fluctuate between -5% and +5% around base
    if (!history[i]) continue;

    history.push(history[i] + parseFloat(change));
    
    const volatilityMultiplier = (Math.random() > 0.7) ? 1 : Math.pow(2, i);
    let priceChange = change * volatilityMultiplier;
    if (priceChange < -5) priceChange *= -1; // Ensure negative changes are possible

    history.push(history[i] + parseFloat(priceChange));
  }

  return { symbol: symbol.toLowerCase().replace(/[^a-z0-9]/gi, ''), name: `Seed ${symbol}`, marketCapUsd: Math.floor(Math.random() * 50000), preRevenuePct: (Math.random() > 0.7) ? 12 : -8 }; // Pre-revenue percentage
}

/**
 * Returns a mock stock tickers list with realistic historical data to simulate 
 * volatility without external API latency during MVP deployment.
 */
function getStockTickers(): { [key: string]: StockData }[] {
  const tics = generateStockHistory('AAPL'); // Apple as seed startup
  
  return Object.entries(tics).map(([symbol, history]) => ({
    ticker_symbol: symbol.toUpperCase(),
    name: `Seed ${symbol}`,
    marketCapUsd: Math.floor(Math.random() * 5000),
    preRevenuePct: (Math.random() > 0.7) ? 12 : -8, // Pre-revenue percentage
    eps_estimate_per_share: history[history.length - 1] / 365 + parseFloat((Math.random() * 4).toFixed(2)),
    risk_rating: Math.random() < 0.9 ? 'Low' : (Math.random() > 0.7) ? 'Medium' : 'High',
  }));
}

/**
 * Simulates an IPO event handler function that fetches real-time tickers 
 * when a user clicks on any stock in the market to trigger price updates.
 */
function handleIPO(symbol: string): void {
  console.log(`[Stock Market Engine] Fetching live data for ${symbol.toUpperCase()}...`);

  const ticker = getStockTickers()[symbol];
  
  // Simulate a slight delay before updating prices (1 second) to mimic network latency
  setTimeout(() => {
    if (!ticker) return;

    console.log(`[Stock Market Engine] Updating price for ${ticker.ticker_symbol}`);
    
    ticker.marketCapUsd = Math.floor(Math.random() * 5000 + 2000); // Slight fluctuation to simulate market movement
    
    // Simulate volatility based on recent performance (1-3 days)
    const previousPrice = history[ticker.symbol];
    let change = ((ticker.marketCapUsd - previousPrice) / previousPrice * 5).toFixed(2);
    
    if (!history[previousPrice]) {
      console.log(`⚠️ WARNING: No price data available for ${symbol.toUpperCase()}`);
      ticker.risk_rating = 'High'; // Warn user about missing historical data before updating prices
      
      return; 
    }

    const newHistory = [...history];
    if (change > 0) {
      newHistory.push(newHistory[newHistory.length - 1] + parseFloat(change));
    } else {
      newHistory.pop(); // Remove last entry to maintain history length consistency for calculation
    }

    ticker.historyEndPrice = newHistory[newHistory.length - 1];
    
    console.log(`[Stock Market Engine] Updated ${ticker.ticker_symbol} price: $${Math.floor(ticker.marketCapUsd / 365).toFixed(2)}`);
