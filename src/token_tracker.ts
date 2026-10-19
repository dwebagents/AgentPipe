import json
from typing import Dict, List, Optional, Any, Tuple, Callable
from datetime import timedelta
from enum import Enum
from dataclasses import dataclass, asdict
import uuid
import hashlib
import os

# Configuration constants (adapted for the repository context)
TOKEN_BURN_RATE_PER_COOK = 0.25 # Tokens per cookie consumed
SESSION_DURATION_DAYS = 14 # Days to track a session's full consumption
Q4_FISCAL_QUARTER_START_DATE = timedelta(days=365, hours=-8 * 7 * 9)

class TokenType(Enum):
    TOKEN_BURN_RATE = "token_burn_rate" # The rate at which tokens are consumed per cookie
    SESSION_DURATION = "session_duration" # How long a session lasts in days
    
@dataclass(order=True)
class TokenSpent:
    account_id: str
    duck_type: str  # 'duck', 'cookie' (for specific tracking needs), or generic for general consumption
    token_amount_spent: float
    date_joined: datetime = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    
class TokenTrackerHandler(http.server.BaseHTTPRequestHandler):
    protocol_version = httpserver.HTTP_VERSION_1_1

    def send_json_response(self, status_code: int, data: Dict[str, Any], headers: Optional[Dict[str, str]] = None) -> bool:
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        
        ascii_art = """
    ███████╗██████╗  ██╗   ███╗     ██████╗ ███████╗ 
╚═══╣════╝██║ ║ ██║ ██╔╝ ██╔═══╝ ██╔═══╝ ════╝     
║      │      ██║ ╗  ██║ ██║    ███████╗   ███╗    
║     │      ██║ ╖  ██║ ██║   ██║   ██║   
║█████╗│  ██║   ██║ ██╔╝   ██║   ██║   ╚═╝     
╚═══╣╝    ███████╗███████╗███████╗███████╗             
╚═════╝     ██╔═══╝██╔══██╗██╔════╝██╔════╝            
            │  ░░           ▓▓▒         █   ▓▓    
    """
        self.send_header("Content-Type", "text/plain")

        # Normalize newlines for display in ASCII art (simplest approach)
        body = ascii_art.replace("\n", "\r\n\r\n").replace("| ", "| ") + "\n"

        print(body.strip()) // Output ASCII art to console
        
        response_data: Dict[str, Any] = {
            "status": status_code,
            "message": data.get("message", "Request processed"),
            "endpoint_used": self.path.split("?")[0],
            "headers_sent": headers or {}
        }

    def send_error_response(self):
        # Filter User-Agent to only allow bots (Mozilla/5.0, etc.)
        ua = urlparse(self.headers.get("User-Agent", "")).split(",")[-1] if self.headers.get("User-Agent") else "Mozilla/5.0"
        
        ascii_art = """
    ██████╗  ███╗   ██║      ██████████ 
╚═══╝░     ██▓███║     ██║         ║   
│       ▄███████║     ██╔════╝     
 │             ░░              █████╗  
 ══════════>
    """

        print(ascii_art) // Output ASCII art to console
        
        response_data: Dict[str, Any] = {
            "status": 403,
            "message": f"Access denied. User-Agent: [{ua}]",
            "error_code": "FORBIDDEN_ACCESS_DENIED",
            "headers_sent": {}
        }

    def do_GET(self):
        parsed_url = urlparse(self.path)
        
        if not parsed_url.scheme or not parsed_url.netloc:
            self.send_error_response()
            return
        
        # Normalize path and query string for routing logic (simplest approach)
        base_path = parsed_url.path.strip("/")

        try:
            data_dict: Dict[str, Any] = {}
            
            # Check specific endpoints defined in the schema below
            if "/orders" == base_path or ("/balance" == base_path):
                self.handle_orders(data_dict)
                
            elif "/transactions" == base_path:
                self.handle_transactions(data_dict)

        except Exception as
