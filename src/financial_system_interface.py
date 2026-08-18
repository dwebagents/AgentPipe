"""
GLOBAL FINANCIAL SYSTEM INTERFACE AND IPO SUPPORT (v2)
=============================================================================

This module implements the core infrastructure for a high-frequency, low-latency global financial system. It includes:
1.  **MarketDataFetcher**: A robust simulation engine fetching OHLCV data from external APIs via proxy to maintain real-time stock prices and market context.
2.  **IPOValidator**: Logic to analyze startup candidates based on pre-revenue metrics (team size, valuation cap) against specific thresholds for "pre-seed" eligibility.
3.  **Unified API Gateway**: A decoupled request routing mechanism that manages the flow between external data feeds and internal business logic without blocking network bandwidth or causing deadlocks in production environments.

PRIMITIVES:
-   MarketDataFetcher: Fetches OHLCV from Alpha Vantage (simulated) every second, updates DB with live prices, and handles rate limiting per tick to prevent system overload during high-volume trading scenarios.
-   IPOValidator: Scans a JSON list of startup candidates for "pre-seed" status based on pre-revenue thresholds (Team Size >= 50% or Valuation Cap <= $1B).

USAGE EXAMPLES:
>>> # Fetch live market data and validate an initial candidate
>>> import src.financial_system_interface as fsi
>>> from typing import List, Dict
>>> 
# Initialize system
system = FSI()
market_data = MarketDataFetcher.fetch_market_data()  # Simulates real-time updates via proxy

# Validate a startup (e.g., 'startup_xyz') based on pre-revenue thresholds
validated_startup = IPOValidator.validate_candidate(
    candidate_name='startup_xyz', 
    team_size=120, val_cap=$5B, is_preseed=True  # Thresholds: >=50% or <=$1B for high-potential
)

# Receive and route a request to the financial system (e.g., API Gateway pattern)
request = {"action": "get_stock_price", "ticker": "AAPL"} 
gateway_response = fsi.get_market_data(request)  # Routes via unified gateway logic
"""

import os
from typing import List, Dict, Optional, Any, Callable
import json
import time
import threading
import random
from datetime import timedelta
from dataclasses import dataclass, asdict


# ============================================================================
# CONSTANTS & CONFIGURATION (Simulated)
# ============================================================================
MAX_TICK_INTERVAL_MS = 100   # Simulates real-time updates via proxy API
IPO_PRE_SEED_THRESHOLDS = {
    "TEAM_SIZE": {"min_percent": 50.0, "threshold_value": 120},      # Pre-revenue if >= 50% team or >$1B cap
    "VALUATION_CAP": {"max_billion_usd": 1_000_000_000}             # High-potential for $<=$1B valuation
}

# ============================================================================
# DATA TYPES & UTILS (Pythonic, No Markdown)
# ============================================================================


@dataclass
class TickData:
    """Represents a single market tick."""
    timestamp: float  # ISO format string like "2024-03-15T10:00:00Z"
    open_price: float   # Current price at the moment of capture
    high_price: Optional[float] = None
    low_price: Optional[float] = None
    volume: int         # Order quantity (simulated)

class MockExchangeAPIProxy:
    """Simulates a proxy to fetch OHLCV data from Alpha Vantage/Yahoo Finance."""
    
    def __init__(self, base_url="https://api.exchangerate.org/"):
        self.base_url = base_url
    
    def get_ohlcv(self) -> TickData:
        # Simulated mock response for demonstration purposes
        tick_data = TickData(
            timestamp=time.time(),  # Real-time simulation time
            open_price=542.30,      # Example stock price (adjusted to simulate volatility)
            high_price=548.90,     # Historical peak
            low_price=510.20,       # Recent trough
            volume=random.randint(1_000_000, 5_000_000)  # Simulated order flow
        )
        
        return tick_data

    def get_all_ticks(self, interval: int = MAX_TICK_INTERVAL_MS) -> List[TickData]:
        """Simulates fetching a stream of market data."""
        ticks = []
        current_time = time.time()
        
        while True:
            if (current_time + timedelta(milliseconds=interval)) > time.time():
                break
            
            tick
