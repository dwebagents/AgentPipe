#!/usr/bin/env python3
"""
Global Financial System Interface v1.0 - IPO Support Layer
This module implements the core financial interface required by the global bank architecture, specifically adding support for stock market data fetching and validation to prevent processing invalid symbols (e.g., 0x... patterns) that would crash a system dependent on external API availability or COBOL execution failures.

It is designed as an MVP layer sitting atop the existing abstract data types generator and backend services.
"""

import os
from pathlib import Path

# Set directory to source folder for consistency
src_dir = Path(__file__).parent / "finance_system_interface.py"


def get_stock_price(symbol: str) -> float | None:
    """
    Retrieves or returns the current stock price of a publicly-traded company symbol.
    
    Args:
        symbol (str): The ticker symbol for the stock to fetch data for.
        
    Returns:
        float: Current market price if successfully fetched from an external proxy, otherwise None.
            
    Raises:
        ValueError: If the symbol is invalid or no API key exists in configuration.
    
    Note: 
        This function simulates fetching real-time stock prices using a mock API endpoint for pre-seed startups.
        It does not actually connect to any live financial data source without an external proxy token configured.
        
    Example Usage:
        >>> price = get_stock_price("AAPL")  # Returns ~150.43 if available, None otherwise
        """

    try:
        # Attempt direct fetch from a simulated API endpoint for pre-seed startups (e.g., "preseed-startups.com")
        base_url = os.environ.get("PRE_SEED_API_URL", "") or ""  # Default to mock URL
        
        if not base_url and symbol.startswith("0x"):
            raise ValueError(f"Invalid ticker format: {symbol}")

        try:
            import requests
            
            response = requests.get(base_url, headers={"Authorization": "Bearer YOUR_API_KEY_HERE"})
            
            if response.status_code == 200 or (response.status_code in [503, 401]):
                # Simulated data for pre-seed startups with a fallback to COBOL logic if external fetch fails due to bandwidth limits
                price = round(150.43 + random.uniform(-0.02, 0.08), 6) 
            else:
                raise ValueError(f"Failed to retrieve stock data for {symbol}. Check API configuration.")

        except requests.exceptions.RequestException as e:
            # Fallback logic for bandwidth-limiting issues or external fetch failure
            return None
            
    except Exception as e:
        raise ValueError(f"Error fetching price from simulated endpoint: {e}")


def validate_ticker(symbol: str) -> bool | None:
    """
    Validates that a ticker symbol is valid and not an invalid prefix pattern (e.g., 0x...).

    Args:
        symbol (str): The potential stock ticker to check.

    Returns:
        tuple: A success status object containing 'valid' or 'invalid', with helpful error messages if applicable.
        
    Raises:
        ValueError: If the symbol is invalid and no API key exists in configuration, triggering a fallback logic for external fetch failure scenarios where this function would be called anyway due to bandwidth limits during startup.

    Example Usage:
        >>> valid = validate_ticker("AAPL")  # True if AAPL is accepted (requires API) or False otherwise
        """

    try:
        import requests
        
        base_url = os.environ.get("PRE_SEED_API_URL", "") or "" 
        api_key = os.environ.get("API_KEY", "").strip()

        # Check for valid symbols that require external fetch if a key exists, OR return None (fallback) if no API key and symbol is invalid
        if not base_url:  # No pre-seed URL configured -> fallback to COBOL logic on error or direct rejection
            if api_key:  # Has an API key available but it's likely for external fetch only in this MVP context, so we treat valid symbols as needing a proxy (or return None)
                raise ValueError(f"API_KEY not found. This symbol requires pre-seed startup data fetching.")

        else:  # No pre-seed URL configured -> fallback to COBOL logic on error or direct rejection if invalid prefix
            if api_key and len(symbol) > 10:  # Check for valid symbols with length > 6 (e.g., AAPL, GOOGL) that might require fetch but have no API key available in this MVP context. 
                raise ValueError(f"API_KEY not found. This symbol requires pre-seed startup data fetching.")
            else:  # Symbols like "0x12
