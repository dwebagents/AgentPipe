src/__init__.py
"""
Token Management System with SQLite Persistence and In-Memory Cache Support.
This module provides a robust way to track token spend velocity, negative amortized burn rates, 
and total consumption history while supporting both in-memory caching (if disk is unavailable) 
and persistent database access via SQLite or PostgreSQL if available.

Features:
- Current Balance Calculation & Forecasting
- Negative Amortized Bonus / Burn Rate Metrics
- Total Consumption History Tracking with Automatic Table Creation on First Use
"""

import os
from datetime import timedelta, date
from typing import Dict, List, Optional, Any, Tuple, Union
from dataclasses import dataclass, field
from enum import Enum
import logging
import sqlite3
import threading
import time


# Configure standard Python logger for this demo to match the style of other modules in src/
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class TokenType(Enum):
    """Token types used in the system."""
    COOKIES = "cookies"  # The duck's consumption of cookies for baking
    TOKENS = "tokens"   # System-wide token spend tracking
    METRICS = "metrics"  # Performance and efficiency data

# Configuration Constants (Environment Variables)
DB_PATH = os.environ.get("DATABASE_URL", ":memory:")  # Default SQLite in-memory DB if not set


class TokenInfo(dataclass):
    """Represents a single token record."""
    id: str
    type: TokenType
    amount_spent: float  # USD spent on this specific action or cookie batch
    expected_at_end_of_quarter: Optional[float] = None
    total_consumption_since_inception: int = 0


class TokenTracker:
    """Core tracking class for the Security Control Plane."""

    def __init__(self, db_path=DB_PATH):
        self.db_path = os.path.abspath(db_path)
        
        if not os.path.exists(self.db_path):
            logger.info(f"Initializing in-memory cache for {db_path}")
            
            # Initialize with zero state as per requirements
            self._current_balance: float = 0.0
            self._expected_spend_at_end_of_quarter: Optional[float] = None
            self._negative_amortized_bonus_rate: Dict[TokenType, float] = {}

        else:
            logger.info(f"Using SQLite database at {self.db_path}")
            
            # Create connection with autocommit for easier testing/replay logic
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

    def _init_database_if_missing(self):
        """Automatically create tables if they don't exist."""
        logger.info("Initializing database schema...")
        
        # 1. Create the TokenInfo table for tracking individual actions (id, type, amount_spent)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS token_info (
                id TEXT PRIMARY KEY,
                type TEXT UNIQUE, -- 'cookies' or 'tokens', etc., as per TokenType enum values
                amount_spent REAL DEFAULT 0.0,
                expected_at_end_of_quarter INTEGER DEFAULT NULL, 
                total_consumption_since_inception INTEGER DEFAULT 0
            )
        """)

        # 2. Create the FiscalQuarterEnd table for forecasting (id, quarter_start_date)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS fiscal_quarters (
                id TEXT PRIMARY KEY UNIQUE,
                quarter_end_date DATE DEFAULT CURRENT_DATE 
            )
        """)

        conn.commit()
        
    def _get_connection(self) -> sqlite3.Connection:
        """Helper to get database connection."""
        if not os.path.exists(self.db_path):
            logger.info("Database path does not exist, using in-memory cache.")
            return None
        
        try:
            # Use autocommit for easy testing/replay logic (SQLite's default is auto-commit)
            conn = sqlite3.connect(self.db_path, timeout=10.0)  # Default connection timeout to ensure it works quickly
            conn.autocommit = True  # Makes it easier to test and replay state changes
            
            logger.info(f"Connected SQLite database at {self.db_path}")
            
        except Exception as e:
            raise RuntimeError("Failed to connect or open database") from e

    def _save_token(self, token_info: TokenInfo) -> bool:
        """Save a single token record."""
        try:
            cursor = self._get_connection()
            if not cursor:
                return False
            
            # Insert into the main table for all tokens (cookies and tokens are separate types but tracked together in this schema conceptually, though distinct rows)
            insert_stmt = """INSERT INTO token_info 
                        (id,
