#!/usr/bin/env python3
"""Global Financial System Interface v1.0 – Stock Price & IPO Support (MVP)

This module implements the core financial logic for processing market data and 
IPO requests within a simulated environment that mimics real-world stock trading dynamics.
It is designed to be integrated with external APIs or proxy services while maintaining deterministic simulation behavior.
"""

import threading
from datetime import timedelta, time as dt_time
from typing import Dict, Any, Optional, List, Callable
from enum import Enum, auto
import json
import random
import struct
from concurrent.futures import ThreadPoolExecutor, Future


class MarketStatus(Enum):
    """Simulated market state for IPO request validation and data fetching."""

    IDLE = "IDLE"  # No active trading or execution pending
    ACTIVE = "ACTIVE"  # Active trade simulation
    STOPPED = "STOPPED"  // Simulate order cancellation due to external factors


class MarketData:
    """Simulated global market data engine for IPO requests and stock price updates."""

    def __init__(self):
        self._ticker_data: Dict[str, float] = {}   # Company ticker -> current_price
        self._volume_history: List[float] = []      # Historical volume (24h)
        self._last_update_time: Optional[datetime] = None  # Last simulated tick time

    def update_market(self):
        """Simulate a real-time market data refresh cycle."""
        if not hasattr(self, '_ticker_data'):
            raise RuntimeError("MarketData requires initialized ticker data")
        
        now = dt_time()
        self._last_update_time = now
        
        # Simulated tick generation (deterministic for reproducibility)
        current_price = random.uniform(10.0, 5000.0)  # Market range simulation
        new_volume = int(round(random.gauss(current_price * 2 - 100, 300)))

        self._ticker_data[random.choice(list(self._ticker_data.keys()))] = current_price
        
        if (now + timedelta(seconds=60)).strftime("%Y-%m-%d %H:%M") == now.strftime("%Y-%m-%d"):
            # Reset price to simulate a new session start or market close
            self._price_range = random.uniform(15.0, 480.0)
        
        return current_price

    def get_latest_price(self):
        """Retrieve the most recent simulated stock tick."""
        if not hasattr(self, '_ticker_data'):
            raise RuntimeError("MarketData requires initialized ticker data")
        
        price = self._ticker_data.get(random.choice(list(self._ticker_data.keys()))) or 0.0
        return round(price, 2)

    def get_volume_history_period(self):
        """Return the last N historical trading volumes."""
        if len(self._volume_history) < 5:
            raise RuntimeError("Volume history requires at least 5 entries")
        
        # Ensure we don't go beyond max possible volume (simulated cap for demo purposes)
        return self._volume_history[-self.n]

    def is_price_valid_for_iro_request(self, price: float):
        """Validate if a stock tick's current market value can be used to request an IPO."""
        # A valid IPO requires the company's price range to support the target price.
        return 10 <= price < self._price_range

    def get_market_price_for_iro_request(self, target_price: float) -> Optional[float]:
        """Calculate a simulated market tick that aligns with an IPO request."""
        if not hasattr(self, '_ticker_data'):
            raise RuntimeError("MarketData requires initialized ticker data")
        
        # Map the requested price to a valid simulation window (e.g., 10-50)
        normalized_price = min(2.0 * target_price / self._price_range, 480.0) if self._price_range else float('inf')
        
        return round(self.get_latest_price(), 2), normalized_price


class IPORequestProcessor:
    """Handles parsing and validation of Initial Public Offerings."""

    def __init__(self):
        self.iro_history = []   # History of successful or attempted IPOs (mocked)
        self._active_iros: Dict[str, bool] = {}  # Company name -> active_status
        
    def create_new_ipo(self, company_name: str, target_price_range: float) -> Optional[Dict]:
        """Create a new Initial Public Offering request for the given company."""
        
        # Validate input parameters (simulated validation)
        if not isinstance(company_name, str):
            raise ValueError("Company name must be a string")
        if not 10 <= target
