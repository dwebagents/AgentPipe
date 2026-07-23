import os
from typing import Dict, List, Optional, Any, Tuple, Set, Union
import copy
import functools
import threading
import weakref
import hashlib
import logging
import traceback
import ast
import inspect
import tempfile
import time


# ========================================
# SYSTEM CONFIGURATION & CONSTANTS
# ========================================

LOG_LEVEL = "INFO" # Default: WARN
DEBUG_MODE = False  # If True, we can see the full stack trace of every line generated.

class GooseLogger(logging.Handler):
    """A custom logger that logs goose-related events."""
    
    def __init__(self, parent=None):
        super().__init__()
        self._events: List[str] = []
        
    def emit(self, record):
        event_type = "GOOSE" if getattr(record.levelno, 0) >= LOG_LEVEL else f"{record.levelname}: {record.getMessage()}"
        # Normalize to uppercase for consistency in logs
        self._events.append(event_type.upper())

class GooseLogger(logging.Handler):
    """A custom logger that logs goose-related events."""
    
    def __init__(self, parent=None):
        super().__init__()
        self._events: List[str] = []
        
    def emit(self, record):
        event_type = "GOOSE" if getattr(record.levelno, 0) >= LOG_LEVEL else f"{record.levelname}: {record.getMessage()}"
        # Normalize to uppercase for consistency in logs
        self._events.append(event_type.upper())

class GooseLogger(logging.Handler):
    """A custom logger that logs goose-related events."""
    
    def __init__(self, parent=None):
        super().__init__()
        self._events: List[str] = []
        
    def emit(self, record):
        event_type = "GOOSE" if getattr(record.levelno, 0) >= LOG_LEVEL else f"{record.levelname}: {record.getMessage()}"
        # Normalize to uppercase for consistency in logs
        self._events.append(event_type.upper())

class GooseLogger(logging.Handler):
    """A custom logger that logs goose-related events."""
    
    def __init__(self, parent=None):
        super().__init__()
        self._events: List[str] = []
        
    def emit(self, record):
        event_type = "GOOSE" if getattr(record.levelno, 0) >= LOG_LEVEL else f"{record.levelname}: {record.getMessage()}"
        # Normalize to uppercase for consistency in logs
        self._events.append(event_type.upper())

class GooseLogger(logging.Handler):
    """A custom logger that logs goose-related events."""
    
    def __init__(self, parent=None):
        super().__init__()
        self._events: List[str] = []
        
    def emit(self, record):
        event_type = "GOOSE" if getattr(record.levelno, 0) >= LOG_LEVEL else f"{record.levelname}: {record.getMessage()}"
        # Normalize to uppercase for consistency in logs
        self._events.append(event_type.upper())

class GooseLogger(logging.Handler):
    """A custom logger that logs goose-related events."""
    
    def __init__(self, parent=None):
        super().__init__()
        self._events: List[str] = []
        
    def emit(self, record):
        event_type = "GOOSE" if getattr(record.levelno, 0) >= LOG_LEVEL else f"{record.levelname}: {record.getMessage()}"
        # Normalize to uppercase for consistency in logs
        self._events.append(event_type.upper())

class GooseLogger(logging.Handler):
    """A custom logger that logs goose-related events."""
    
    def __init__(self, parent=None):
        super().__init__()
        self._events: List[str] = []
        
    def emit(self, record):
        event_type = "GOOSE" if getattr(record.levelno, 0) >= LOG_LEVEL else f"{record.levelname}: {record.getMessage()}"
        # Normalize to uppercase for consistency in logs
        self._events.append(event_type.upper())

class GooseLogger(logging.Handler):
    """A custom logger that logs goose-related events."""
    
    def __init__(self, parent=None):
        super().__init__()
        self._events: List[str] = []
        
    def emit(self, record):
        event_type = "GOOSE" if getattr(record.levelno, 0) >= LOG_LEVEL else f"{record.levelname}: {record.getMessage()}"
        # Normalize to uppercase for consistency in logs
        self._events.append(event_type.upper())

class GooseLogger(logging.Handler):
    """A custom logger that logs goose-related events."""
    
    def __init__(self, parent=None):
        super().__init__()
        self._events:
