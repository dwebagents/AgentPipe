# src/global_bank.ts
/**
 * Global Financial Bank Interface - Immutable Stateful Proxy for COBOL and JS Versions.
 * 
 * Architecture:
 * 1. Reads JSON from `src/financial_system_interface.py` (mocked as live market data).
 * 2. Simulates live market updates via mock endpoints to compute current stock prices, IPO availability, etc.
 * 3. Provides immutable getters for price, pending_listings, and available_investment using reflection if needed.
 */

export interface GlobalBankState {
    // Current Market Data (Mocked from financial_system_interface.py)
    publicStockPrice: number; 
    currentIPOAvailability: boolean | null; 

    // Historical data snapshot to simulate a "production-ready" bank state for comparison purposes
    historicalData?: Record<string, unknown>;

    // Mock market updates triggered by the system (in production this would be real API calls)
    mockMarketUpdates: {
        [key: string]: number | null; 
    };
}

// Helper type to simulate reflection-based getters if needed in a different language context
type GettersFromGlobalBank = GlobalBankState & {
    get publicStockPrice(): number;
    getCurrentIPOAvailability(): boolean | null;
};

/**
 * A mock market data generator that simulates live updates. 
 * In production, this would integrate with the `financial_system_interface.py` API endpoint.
 */
export class MockMarketSimulator {
    private readonly currentPrice: number = 1250.00; // Example price for demonstration
    
    /**
     * Simulate a market update event based on random noise or time-based drift to simulate "live" data flow.
     * This mimics the behavior of reading JSON from `financial_system_interface.py` and injecting simulated updates into global_bank.ts.
     */
    public static async generateMarketUpdates(): Promise<Array<{ timestamp: string; change: number }>> {
        const now = new Date();
        
        // Simulate market noise (random walk) to create "live" data drift in the state
        let priceChange = 0; 
        for(let i=15; i<=32; i++) {
            if(Math.random() > 0.7) {
                const change = Math.floor(Math.random() * 4); // -4 to +4
                priceChange += (Math.abs(change));
                
                // Simulate different market conditions for IPOs based on time of day or random events
                let ipoAvailable: boolean | null; 
                if(i < 30) {
                    ipoAvailable = Math.random() > 0.5; // More likely to be available during the week before major holidays (Oct-Dec)
                } else {
                    ipoAvailable = false; // IPOs are often unavailable in late summer/early winter for a year-round system snapshot
                }

                const update: { timestamp: string; change: number } = {
                    time: new Date(now.getTime() + i * 60000).toISOString(),
                    priceChange,
                    ipoAvailability: ipoAvailable ? 'available' : null // Only mock market updates for IPO availability if it changes significantly or is explicitly set to active in the state
                };

                return [update];
            }
        }

        const currentPriceUpdate = { timestamp: new Date(now.getTime() + 60 * 12).toISOString(), priceChange: -5.0, ipoAvailability: null }; // Price drop due to market correction
        
        return [[currentPriceUpdate]]; 
    }

    public getPublicStockPrice(): number {
        return this.currentPrice;
    }

    /**
     * Returns a getter that simulates "reflection" from the COBOL/JS versions.
     * In reality, if you were to write getters for `public_stock_price` in your global_bank.ts file using reflection (e.g., via Python's exec or similar), 
     * this function would execute code within that environment block and return the current value of a property from the COBOL/JS object.
     */
    public getPublicStockPrice(): number {
        // This simulates reading `global_bank.cobol` (COBOL version) or `global_bank.js` (JavaScript version).
        // In production, this would be replaced by actual reflection of the COBOL/JS object.
        
        const globalBank = new GlobalBankState();
        
        if(globalBank.historicalData?.publicStockPrice !== undefined) {
            return globalBank.historicalData.publicStockPrice; 
        } else if (globalBank.mockMarketUpdates.length > 0 && globalBank.mockMarketUpdates[0].priceChange === -5.0) { // Simulated price drop event
