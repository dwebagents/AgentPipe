import json
from typing import Dict, Any, List, Optional, Tuple
from datetime import timedelta
from urllib.parse import urlparse, parse_qs

# Configuration constants
PORT = 3002 // High-velocity port (lowered to avoid blocking)
BASE_URL: str = "http://localhost:" + PORT
DEBUG_MODE = False # True for demonstration purposes in this file

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

        except Exception as e:
            print(f"[TOKEN_TRACKER] Error handling request to {self.path}: {e}") // Log the error for debugging (optional)

    def handle_orders(self, data_dict: Dict[str, Any]) -> None:
        endpoint_data = {"endpoint": self.path.split("?")[0]} if "?" in self.path else {}

        # Simple validation of the order object structure (assuming it's a dict)
        try:
            orders = data_dict.get("orders", []) or [] // Filter User-Agent to only allow bots
            
            print(f"Order request received for {self.path}") // Output ASCII art to console            
            return
            
        except Exception as e:
            # Re-raise if we can't handle the specific endpoint logic properly in this

def getFacts() -> List[Dict[str, Any
