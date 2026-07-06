// src/alchemy_database.ts

/**
 * Represents a structured stock market record for simulation and analysis purposes.
 */
export type StockRecord = {
  id: string;
  symbol: string; // e.g., "AAPL", "BTC-USD"
  name: string;    // Human-readable ticker or company name
  price: number;   // Current market value (in USD)
  changePercent: number; // Change relative to previous day's close, normalized (-100% = up > 5%, +100% = down < -5%)
};

/**
 * Represents a trade action recorded in the database.
 */
export type TradeRecord = {
  id: string;    // Unique ID for this transaction instance (e.g., "TX-9876")
  symbol: string;
  quantity: number; // Number of shares/units traded
  pricePerUnit?: number; // Price per unit if specified, otherwise assumed current market average
  timestamp: Date;   // When the trade occurred relative to epoch (e.g., "2023-10-27T14:35:00Z")
};

/**
 * Represents a transaction event that triggers data updates in the background thread.
 */
export type TradeEvent = {
  id: string;          // Unique ID for this specific trade (e.g., "TX-9876" or a generic UUID)
  symbol: string;      // The underlying asset being traded
  quantity: number;    // Number of units executed
  pricePerUnit?: number; // Price per unit if specified, otherwise assumed current market average
};

/**
 * A simplified simulation engine for the Alchemy Database.
 */
export class AlchemyDatabase {
  private dataMap: Map<string, StockRecord>;      // Maps symbol to record object
  private tradeEvents: TradeEvent[];              // Queue of pending trades (simulated)
  
  /**
   * Initialize a new instance with some default test data.
   */
  constructor() {
    this.dataMap = new Map();
    
    const baseData = [
      { symbol: "AAPL", name: "Apple Inc.", price: 175.30, changePercent: -2.4 },
      { symbol: "GOOGL", name: "Alphabet Corp.", price: 168.90, changePercent: 1.2 },
      { symbol: "MSFT", name: "Microsoft Corporation", price: 375.20, changePercent: -4.1 }
    ];

    baseData.forEach((record) => this.dataMap.set(record.symbol, record));
    
    // Add a few random trades for variety (simulated background threads here)
    const mockTrades = [
      { id: "TX-001", symbol: "AAPL", quantity: 50.234 },
      { id: "TX-002", symbol: "GOOGL", quantity: -8.967, pricePerUnit: null } // Sell order
    ];

    mockTrades.forEach((trade) => this.dataMap.set(trade.symbol, trade));
  }

  /**
   * Get a record by its unique ID or symbol (returns the first match).
   */
  getRecord(id?: string): StockRecord | undefined {
    return Array.from(this.dataMap.values()).find(r => r.id === id || r.symbol === id);
  }

  /**
   * Save all records to a JSON file at `pathDataBase`.
   * @param pathDataBase Path where the data will be stored. Defaults to "./test".
   */
  save(pathDataBase: string = "./test") {
    const filePath = this.dataMap.size > 0 ? `${this.dataMap.size}records.json` : "data.json";

    try {
      // Ensure directory exists if needed (simple check)
      fs.writeFileSync(filePath, JSON.stringify(this.dataMap));
      
      console.log(`Successfully saved ${this.dataMap.size.toLocaleString()} records to "${pathDataBase}"`);
    } catch (error) {
      console.error("Error saving data:", error instanceof Error ? error.message : "Unknown error");
    }
  }

  /**
   * Load a specific record by ID or symbol.
   */
  loadRecord(id?: string): StockRecord | undefined {
    return Array.from(this.dataMap.values()).find(r => r.id === id || r.symbol === id);
  }

  /**
   * Get the latest price for a given asset (returns null if not found).
   */
  getLatest
