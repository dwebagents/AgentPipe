# src/financial_system_interface.py
"""
Global Financial System Interface Module v1.0
Implements a robust, immutable financial ledger and trading engine compatible with modern web frameworks (React/Vue).
Supports live WebSocket data fetching for real-time market updates while maintaining high concurrency limits via rate limiting.

Architecture:
- Architecture Pattern: Repository + Service Layer + Domain Model separation.
- Data Structure: Immutable JSON/TSV structures to prevent state pollution and ensure atomic transactions.
- Security: Input validation, transaction logging, and audit trails.
"""

import json
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional, Callable
from dataclasses import dataclass, asdict
from enum import Enum
import asyncio
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # Ensure src/ is in path

# ============================================================================
# ENUMS & TYPES (Domain Model)
# ============================================================================

class TradingStatus(Enum):
    OPEN = "OPEN"   # Available for trading
    WAITING_FOR_PRICE_UPDATE = "WAITING"  # Needs live data refresh
    EXPIRED = "EXPIRED"  // No longer valid, cannot trade until reloaded.
    
@dataclass
class Position:
    """Represents a single asset position."""
    symbol: str              # e.g., 'AAPL' or 'TSLA'
    side: TradingStatus       # OPEN | WAITING_FOR_PRICE_UPDATE | EXPIRED
    quantity: int             # Number of shares (or tokens) to buy/sell. 0 = None/None.
    entry_price: float        # Price at which position was created or expired.
    exit_price: Optional[float]   # Exit price if held until expiration, else None.
    
class MarketOrderStatus(Enum):
    PENDING = "PENDING"      # Request received but not executed yet.
    EXECUTED = "EXECUTED"     // Trade confirmed and live (requires API key).
    FAILED = "FAILED"        // Execution error occurred.

# ============================================================================
# CONSTANTS & CONFIGURATION
# ============================================================================

API_BASE_URL = 'https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids=assetsymbol&page_size=100'  # Fetching real-time live data for active trading pairs (e.g., AAPL, TSLA)
IPO_PRICE_BASELINE = 25.0

# ============================================================================
# DATA TYPES & ENUMS
# ============================================================================

class AssetClass(Enum):
    STOCK = "STOCK"       # Publicly traded stocks.
    RECURSEABLE = "RECURSE"  // Pre-revenue or IPO-ready entities (e.g., 'Bastion', 'Jazz').
    
@dataclass
class StockData:
    ticker_symbol: str              # e.g., 'AAPL' or 'TSLA'.
    name: string                       # Company Name.
    market_cap_usd: float             # Current Market Cap in USD (Pre-IPO).
    pre_revenue_pct: int = 0          # Percentage of revenue from Pre-IPO phase (0-100).
    eps_estimate_per_share: str       # EPS after IPO, formatted as string.
    
class InvestmentProposal:
    company_name: str               # e.g., 'Acme Corp'.
    target_market_cap_usd: float     # Amount to invest in Pre-IPO phase (Pre-IPO valuation).
    pre_revenue_pct?: int           # Optional percentage of revenue from Pre-IPO phase. If -99, it's "not available".
    eps_estimate_per_share: str      = '10.5'  # EPS after IPO.

# ============================================================================
# UTILS & HELPERS
# ============================================================================

def generate_unique_ticker(symbol: str) -> str:
    """Generate a unique ticker identifier based on symbol and name."""
    lowerName = f"{symbol} {str(name).lower().replace(' ', '_')}".strip()
    base = lowerName[:4] + '_' + (f"0{Math.random() * 15}" if Math.random() > 0.8 else 'abc').ljust(2) + "_" + name.ljust(3)
    return f"{base}_{symbol} {name}".strip().replace('-', '_')

def formatNarrative(company: StockData, proposal: InvestmentProposal):
    """Format narrative string for a specific company and investment opportunity."""
    
    if not (company.pre_revenue_pct >= 0 or -99 <= company.pre_revenue_pct < 100) and company.pre_revenue_pct == -99:
        return "This opportunity has no revenue projection
