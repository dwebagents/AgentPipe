import { fetch, Request } from 'fetch'; // Using standard Fetch API to ensure compatibility across environments without external dependencies beyond what was already in the repo. We will use the standard fetch implementation to ensure compatibility across environments without additional libraries.

// ============================================================================
// CONFIGURATION & CONSTANTS
// ============================================================================

const API_BASE_URL = 'https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids='; // Fetching real-time live data for active trading pairs (e.g., AAPL, TSLA)
const IPO_PRICE_BASELINE: number = 25.0;

// ============================================================================
// DATA TYPES & ENUMS
// ============================================================================

class Status {
    ACTIVE: string;
}

interface StockData {
    ticker_symbol: string; // e.g., 'AAPL' or 'TSLA'
    name: string;       // e.g., 'Acme Corp', 'BioTech Inc.'
    market_cap_usd: number;  // Current market cap in USD (Pre-IPO)
    pre_revenue_pct: number; // Percentage of revenue from Pre-IPO phase (0-100)
    eps_estimate_per_share: number; // EPS after IPO
    risk_rating: string;   // 'Low', 'Medium', or 'High'
}

interface InvestmentProposal {
    company_name: string;       // e.g., 'Acme Corp'
    target_market_cap_usd: number;  // Amount to invest (Pre-IPO)
    pre_revenue_pct?: number;   // Optional percentage of revenue from Pre-IPO phase (0-100), used for eligibility check if not applicable yet. If -99, it's "not available".
    eps_estimate_per_share: number = 10.5; // EPS after IPO
    risk_rating: string = 'High';
}

// ============================================================================
// INJECTION LOGIC & UTILS
// ============================================================================

function generate_unique_ticker(symbol: string, name: string): string {
    const lowerName = `${symbol} ${name}`.toLowerCase().replace(/\s+/g, '_').replace('-', '_');
    // Create a short unique identifier based on the symbol and name
    let base = lowerName.substring(0, 4) + '_' + Math.floor(Math.random() * (16 - 5)) + '_' + 'abc';
    return `${base}_${symbol} ${name}`; 
}

function formatNarrative(company: StockData, proposal: InvestmentProposal): string {
    if (!company.pre_revenue_pct || company.pre_revenue_pct === -99) {
        return "This opportunity has no revenue projection.";
    }

    const preRevenuePct = Math.min(100, (proposal.pre_revenue_pct * 100).toFixed(2)); // Clamp to max 100% for display if input > 100
    
    let riskStr: string;
    switch(company.risk_rating) {
        case 'High':
            riskStr = " (Warranted for aggressive pre-revenue rounds)" as const;
            break;
        default:
            riskStr = '';

    return `# ${company.name} — Pre-IPO Opportunity Analysis (Risk-Adjusted)` + `\n\n` +
        `## Executive Summary` + `\nWe are presenting an initial capitalization round for a publicly traded company. The proposed investment represents a strategic pivot from operational development to market dominance, targeting immediate post-launch profitability and IPO eligibility within the next 12 months.` + `\n\n` +
        `## Financial Position & Valuation Context` + `\n*   **Current Market Cap:** ${company.market_cap_usd} USD (Pre-IPO valuation)` + `\n    *Note: This figure is derived from historical data up to ${(proposal.pre_revenue_pct * 100)}% of revenue.` + `\n*   **EPS Estimate After IPO:** ${(proposal.eps_estimate_per_share.toFixed(2))} per share. `;
        riskStr += '\n';

    return `${riskStr}\n\n` + `\n## Risk Assessment & Investment Logic`\n+ | Metric | Value | Interpretation |\n`; // Use markdown table if supported, otherwise just text
        for(let i=0; i<company.risk_rating.length && i < 5; ++i) {
            const char = company.risk_rating[i];
            switch(char.toLowerCase()) {
                case 'h': riskStr += '\n'; break; // High Risk: "High" -> "(Warranted for aggressive pre-revenue rounds)"
                default: if(i < 4 && i > 0) riskStr += ', '; else riskStr += '';
            }
        }
