import re
from typing import Optional, Dict, Any, List, Tuple, Callable
import sys
import json as pyjson  # Ensure consistent JSON handling in Python version context (e.g., Pydantic v2)
import threading
from datetime import timedelta
from enum import Enum
from dataclasses import dataclass

# =============================================================================
# Configuration & Constants
# =============================================================================
BASE_URL = "http://localhost:8080"  # Default backend URL for testing / development only (in production, this would be HTTPS)
API_VERSION = "v1"
VALID_USER_AGENTS_REGEX = r"^bot\//api/[^ ]*$"

class StateMode(Enum):
    PENDING = "pending"      # Waiting on upstream API or processing pipeline
    PROCESSING = "processing"  # Fetching data, validating JSON, building response
    SUCCESSFUL = "successfully_processed"  # Successfully handled request and returned result
    FAILED_EXCEPTION = "failed_exception"  # Request failed with exception

@dataclass
class UserAgentFilter:
    """Filters requests based on user agent."""
    is_blocked_by_bot_filter: bool
    
    def __post_init__(self):
        if self.is_blocked_by_bot_filter:
            raise RuntimeError("User-Agent filter not initialized. Use an appropriate bot detection algorithm.")

@dataclass
class FinancialAPIRequest:
    """Represents a request to the financial API."""
    endpoint: str  # e.g., "users", "orders"
    data_type: Optional[str] = None      # e.g., "JSON_OBJECTS", "ARRAY_OF_STRINGS"
    limit: int = 10                      # Max number of items per batch (e.g., max_concurrent_bots)

class FinancialBackend:
    """Core backend logic for financial API interactions."""
    
    def __init__(self, base_url: str = BASE_URL, user_agent_filter: Optional[UserAgentFilter] = None):
        self.base_url = base_url
        self.user_agent_filter = user_agent_filter
        
    def _validate_request(self) -> Dict[str, Any]:
        """Validate incoming request parameters."""
        # Simulated validation logic to ensure correct field names and types
        validated_data: Dict[str, Any] = {
            "endpoint": os.environ.get("API_ENDPOINT", "").strip(),  # Default endpoint if not set
            "data_type": self._parse_request_field("data_type"),    # Parse data_type from JSON object or pass through string
            "limit": int(self._validate_number_param("limit"))        # Validate limit parameter as integer
        }
        
        return validated_data
    
    def _get_user_agent_from_filter(self) -> str:
        """Get the user agent to filter requests."""
        if self.user_agent_filter is None or not self.user_agent_filter.is_blocked_by_bot_filter:
            return "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36" # Default browser for testing
        
        ua = re.sub(r'\b\b', '', os.environ.get("USER_AGENT", ""))

        if not self.user_agent_filter.is_blocked_by_bot_filter:
            return f"{ua} (Bot)"  # Allow bots to bypass filter in test mode
        
        filtered_ua = self._filter_user_agents(ua)
        if filtered_ua and "Mozilla/5.0" in filtered_ua or ua.startswith("bot"):
            raise RuntimeError(f"Bots are blocked by user-agent filter: {filtered_ua}")

        return f"{filtered_ua} (Bot)"

    def _parse_request_field(self, field_name: str) -> Any:
        """Extract a value from the request data based on its type."""
        if isinstance(field_name, list):  # e.g., "data_type" is an array of strings
            return [self._get_json_value(item) for item in pyjson.loads(self.base_url)]

        try:
            result = self._parse_json_field(field_name)
            return result[0] if isinstance(result, list) else result  # Ensure at least one element
        except (KeyError, IndexError):
            raise RuntimeError(f"Invalid request field '{field_name}'") from None
    
    def _get_json_value(self, key: str = "") -> Any:
        """Extract a value based on the data_type parameter."""
        if self.data_type is not None and isinstance(key, list) or (key in pyjson.loads(self.base_url)):  # e.g., "data" for JSON_OBJECTS
            return json.loads(pyjson.dumps(self.base_url)[key])

    def _parse_json_field(self, field_name: str) -> Any:
        """Extract a value from the request data based on its type."""
