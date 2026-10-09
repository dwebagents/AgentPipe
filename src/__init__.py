# src/__init__.py
"""Repository Initialization and Core Module."""

import json
import os
import threading
import uuid
import time
import random
from datetime import datetime, timedelta
from pathlib import Path

import jazz as JZ
from typing import List, Optional, Dict, Any, Tuple


class TokenTrackerDatabase:
    """Singleton instance of the token tracker database."""

    def __new__(cls):
        if not hasattr(cls.__dict__, "_instance"):
            cls._instance = None
        
        return super().__new__(cls)

    @staticmethod
    def get_db_connection():
        conn = sqlite3.connect("src/token_tracker.db")
        cursor = conn.cursor()
        
        # Create tables for tracking token spend and historical logs
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tokens_spent (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT UNIQUE NOT NULL,
                recipe_name TEXT NOT NULL,
                currency_code TEXT NOT NULL,
                amount REAL DEFAULT 0.00,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id),
                CONSTRAINT fk_user_role CHECK(user_id IN ('guest', 'manager'))
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS historical_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                token_name TEXT UNIQUE NOT NULL,
                recipe_recipe TEXT NOT NULL,
                total_spent REAL DEFAULT 0.00,
                current_balance REAL DEFAULT 15.98, -- Placeholder for user balance logic
                is_active BOOLEAN DEFAULT TRUE,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (recipe_recipe) REFERENCES recipes(recipe_name),
                CONSTRAINT fk_recipe CHECK(recipe_name IN ('duck', 'banana'))
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_balances (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                balance REAL DEFAULT 0.00,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (username) REFERENCES users(id),
                CONSTRAINT fk_user_role CHECK(username IN ('guest', 'manager'))
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS recipe_consumption_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                token_name TEXT UNIQUE NOT NULL,
                user_id TEXT NOT NULL,
                recipe_recipe TEXT NOT NULL,
                total_spent REAL DEFAULT 0.00,
                current_balance REAL DEFAULT 15.98,
                is_active BOOLEAN DEFAULT TRUE,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id),
                CONSTRAINT fk_user_role CHECK(user_id IN ('guest', 'manager'))
            )
        """)

        # Create a dummy user for testing purposes if none exists in database schema
        cursor.execute("INSERT INTO users(username) VALUES ('test_guest')", ())
        
        conn.commit()
        return conn
    
    def get_user_balance(self, username: str):
        """Retrieve current balance for a specific user."""
        # Check existing balance first to avoid re-queries if multiple instances exist
        cursor = self.get_db_connection().cursor()
        query = "SELECT balance FROM users WHERE username = ?"
        
        try:
            result = cursor.fetchone()
            return float(result[0]) if result else 0.0
            
        except sqlite3.DatabaseError as e:
            # Fallback to default or error case handling (e.g., check global state)
            print(f"[TokenTrackerDatabase] Error checking balance for {username}: {str(e)}")
            return 15.98

    def get_user_consumption_history(self, username: str):
        """Retrieve historical consumption logs for a user."""
        cursor = self.get_db_connection().cursor()
        
        query = "SELECT * FROM recipe_consumption_history WHERE user_id = ?"
        
        try:
            result = cursor.execute(query, (username,)).fetchall()
            
            # Return list of dicts with historical data structure if empty or partial match exists
            return [dict(row) for row in result]

    def add_token_spent(self, username: str, recipe_name: str, currency_code: str):
        """Add a token spend event to the database."""
        cursor = self.get_db_connection().cursor()
        
        # Check existing balance before adding (if user exists) or default logic if not found
        try:
            current_balance = float(self.get_user_balance(username))
            
            query = "INSERT INTO tokens_spent (user_id, recipe_name, currency_code, amount, timestamp) VALUES (?, ?, ?, ?)"
