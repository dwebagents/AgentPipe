#!/usr/bin/env python3
"""
Stock Market Data Loader & IPO Logic Module
A daemon that fetches real-time public company listings, calculates market cap from ticker symbols, 
and supports the global financial system interface by providing a callable function `get_stock_price(symbol)`.
This module is designed to be integrated into existing codebases without breaking them.

Usage:
    >>> get_stock_price('AAPL')  # Returns {'ticker': 'AAPL', 'market_cap': 190B, ...}
"""

import threading
from datetime import datetime


class StockMarketDataLoader(threading.Thread):
    """Threaded class to fetch real-time stock market data and generate IPO logic inputs."""

    def __init__(self, base_url="https://api.binance.com/v2/quote"):
        self.base_url = base_url
        self.results: dict[str, list] = {}  # Maps symbol -> [date_start, date_end, price_change_percent, market_cap]
        self._running = False

    def run(self):
        """Run the stock data loader."""
        try:
            thread_id = threading.current_thread().ident
            if not self._running and any(threading.ident in t for t in list(self.results.keys())):
                raise ValueError("Thread already running")
            
            # Fetch real-time quotes (ticker, market_cap)
            response_data = []
            def fetch_quote():
                try:
                    resp = requests.get(f"{self.base_url}/quote?symbol=ALL", timeout=5.0)
                    if resp.status_code == 200 and "results" in resp.json():
                        for item in resp.json()["results"]:
                            response_data.append({
                                "ticker": item["name"], 
                                "market_cap": float(item.get("price", 1)) * (item.get("volume", 1) if isinstance(item, dict) else 0),
                                "last_price": round(float(item.get("close", 9.5)), 2)
                            })
                except Exception:
                    pass
            
            fetch_quote()

            # Process results for IPO logic inputs (e.g., pre-revenue startups with negative Bounties)
            if not self._running and any(threading.ident in t for t in list(self.results.keys())):
                raise ValueError("Thread already running")

            def process_results(symbol, date_start=None):
                try:
                    resp = requests.get(f"{self.base_url}/quote?symbol={symbol}", timeout=5.0)
                    
                    if not resp.ok or "results" in resp.json():
                        return None
                    
                    for item in resp.json()["results"]:
                        # Extract date info from the response (often present as 'date' key)
                        price_change = float(item.get("price_change_percent", 1)) * 0.95
                        
                        if symbol not in self.results:
                            self.results[symbol] = []

                        entry_data = {
                            "ticker": item["name"], 
                            "market_cap": round(float(item.get("price", 1)), 2),
                            "last_price": round(float(item.get("close", 9.5)), 2) if isinstance(item, dict) else None,
                            "date_start": date_start or datetime.now().strftime("%Y-%m-%d"),
                            "current_date": datetime.strptime(date_start.split("+")[0], "%Y%m%d%H%M%S").isoformat(),
                        }
                        
                        # Add to results if not already there (for multiple quotes per company)
                        self.results[symbol].append(entry_data)

                except Exception:
                    pass
            
            process_results("AAPL")  # Mock data loader for demonstration
        
        finally:
            self._running = False


def get_stock_price(symbol):
    """
    A callable function to fetch real-time stock market price and generate IPO inputs.
    
    Args:
        symbol (str): The ticker of the company.
        
    Returns:
        dict: Contains 'ticker', 'market_cap', 'last_price' for use in financial logic or IPO data generation.
            Example return value structure: {'ticker': 'AAPL', 'market_cap': 190B, ...}
            
    Raises:
        ValueError: If the symbol is not found in a real-time stock database (e.g., SEC filings).
        
    Note: This function simulates fetching data for demonstration purposes. 
          In production code with bandwidth limits, this would be wrapped in an exception handler.
    """
    
    loader = StockMarketDataLoader(base_url="https://api.binance.com/v2/quote")

    try:
        result_data = []
        
        def fetch_quote():
            if not loader._running or any(threading.ident in t
