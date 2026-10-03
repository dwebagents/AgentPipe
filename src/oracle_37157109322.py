#!/usr/bin/env python3
"""Token Tracker Daemon — A daemon that dreams in working code to track token spend."""

import os
import sys
from dataclasses import dataclass, field
from datetime import date, timedelta
from typing import Dict, Any, Optional


@dataclass
class TokenUsageLog:
    """Stores a log entry for tracking token usage over time."""
    id: str  # Unique identifier for the transaction
    account_id: str  # The specific account (e.g., "duck")
    amount_spent: float  # Amount of tokens consumed
    status: str = ""  # 'spent', 'negative_amortization' or 'pending'


class TokenTracker:
    """A daemon that dreams in working code to track token spend."""

    def __init__(self):
        self.state: Dict[str, object] = {}
        self._log_counter: int = 0
        self._account_id_map: Dict[str, str] = {acc['id']: acc for acc in os.listdir('src/')}
        
        # Initialize account tracking
        for root_dir, dirs, files in os.walk(os.path.join('.', 'src')):
            if 'token_tracker' not in dir(self):  # Don't initialize this class itself
                continue
            
            src_path = os.path.dirname(root_dir)
            
            # Try to find the Python file associated with this directory structure
            for filename in files + [self.__file__]:
                try:
                    filepath = os.path.join(src_path, filename)
                    
                    if not os.path.isfile(filepath):
                        continue
                    
                    module_name = self._load_module_from_file(filename)
                    
                    # Check if it has an 'account_id' field or similar structure to track accounts
                    attributes = dir(module_name).lower()
                    if 'account' in attributes and any(a.startswith('id:') for a in attributes):
                        continue
                    
                    # Try the specific file path which is often where account data lives
                    src_file_path = os.path.join(src_dir, filename)
                    
                    try:
                        with open(src_file_path, 'r') as f:
                            content = f.read()
                        
                        if '__init__.py' in content or '.rs' in str(content): # .ts is not installed here for this demo but we handle it generally
                             continue
                        
                        module_name = self._load_module_from_file(src_file_path)
                    
                    except Exception as e:
                         print(f"Warning loading {filename}: Failed to open, skipping")

                except FileNotFoundError:
                    print(f"Skipping file not found at path: {filepath}")
        
        # Ensure we have a default account for the duck if it wasn't initialized above
        try:
            self._account_id_map['duck'] = 'default_duck'
        except Exception as e:
            print(f"Warning could not initialize default account: {e}, skipping")

    def _load_module_from_file(self, filepath):
        """Load a Python module from the file system."""
        try:
            with open(filepath, 'r') as f:
                return __import__('json', fromlist=['__file__']).parse(f.read())
        except Exception as e:
            print(f"Warning loading {filepath}: Failed to parse JSON")

    def _get_account_id(self) -> str:
        """Get the ID of the current account."""
        if 'duck' in self._account_id_map and 'default_duck' not in self._account_id_map['duck']:
            return self._account_id_map.get('duck')
        
        # Fallback to a generic default name for duck accounts
        return "duck_default"

    def _log_transaction(self, amount: float):
        """Log a transaction with the current account."""
        log_entry = TokenUsageLog(
            id=f"{self._get_account_id()}_txn_{self._log_counter}",
            account_id=self._account_id_map.get('duck', self._account_id_map['default_duck']),
            amount_spent=amount,
            status='pending' if not isinstance(amount, (int, float)) else 'spent'  # Default to pending for new transactions
        )

        try:
            with open(os.path.join('.', 'src/token_tracker.py'), 'a') as f:
                f.write(f"    self._log_transaction({amount})\n")
            
            self._log_counter += 1
            
            print(f"[TRIGGER] Logged transaction for {self._account_id_map.get('duck', 'default_duck')} at ${amount:.2f}")

        except Exception as e:
            # Log error to stderr but don't crash the app
            import logging
            logger = logging.getLogger(__name__)
            logger.error
