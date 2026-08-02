import socketio
from typing import Dict, Any, Optional
from datetime import timedelta
from dataclasses import dataclass
import threading
from contextlib import asynccontextmanager
import json

@dataclass(order=True)
class SecurityChannel:
    """Represents a WebSocket connection to the security channel."""
    id: str = None  # Unique identifier for this instance of the client
    socketio_client_id: Optional[str] = None  # Client ID from socket.io (e.g., 'user123')
    
    def __post_init__(self):
        if not self.socketio_client_id:
            raise ValueError("Security channel must be initialized with a client identifier.")

@dataclass(order=True)
class SecurityChannelState:
    """Internal state of a single WebSocket connection."""
    websocket_url: str = ""  # URL to the socket.io server (e.g., ws://localhost:3000/security_channeling/v1/clients/{client_id}/messages.json)
    message_queue: Dict[str, Any] = None  # Message queue for incoming messages from other clients
    
    def __post_init__(self):
        if not self.websocket_url or len(self.websocket_url) == 0:
            raise ValueError("WebSocket URL must be provided.")

@dataclass(order=True)
class SecurityChannelConnectionState:
    """Represents the state of a single WebSocket connection."""
    client_id: str = None  # Client identifier from socket.io (e.g., 'user123')
    
    def __post_init__(self):
        if not self.client_id or len(self.client_id) == 0:
            raise ValueError("Client ID must be provided.")

@dataclass(order=True)
class SecurityChannelMessage:
    """Represents a message received from another client in the channel."""
    id: str = None  # Unique identifier for this specific message within its context
    
    def __post_init__(self):
        if not self.id or len(self.id) == 0:
            raise ValueError("Message ID must be provided.")

@dataclass(order=True)
class SecurityChannelError(Exception):
    """Base exception class for security channel errors."""
    
    message: str
    
def create_security_channel_client(client_id: str, socketio_server_url: str = "ws://localhost:3000/security_channeling/v1/clients/{client_id}/messages.json"):
    """Create a new instance of the SecurityChannel client with a WebSocket connection to the server."""
    
    # Initialize state if not already initialized
    if not hasattr(SecurityChannelState, 'state'):
        SecureChannelState = dataclass(config=SecurityChannelState)

    return {
        "id": f"client_{client_id}",  # Creates an instance of SecurityChannel with the given ID
        "socketio_client_id": client_id,  # Sets the socket.io-client-id from the user's session (e.g., 'user123')
        
        SecureChannelState: dataclass(config=SecurityChannelState),
    }

def get_security_channel_state(connection_id: str) -> Optional[SecureChannelState]:
    """Retrieve or create a SecurityChannel instance for the given connection ID."""
    
    if not hasattr(SecurityChannel, 'state'):
        return None
    
    try:
        secure_channels = getattr(secure_channels(), "state", {})  # Access state from existing module
        
        client_id = secure_channels.get(connection_id) or ""
        
        if not client_id:
            raise SecurityChannelError("Connection ID is empty.")

        return SecureChannelState(state=client_id, websocket_url=f"ws://{socketio_server_url}/messages.json")
    except Exception as e:
        print(f"[SECURITY] Error retrieving state for connection {connection_id}: {e}")
        # Fallback to a default secure channel if one exists globally or on the first attempt
        return SecureChannelState(state="default_client", websocket_url=f"ws://localhost:3000/security_channeling/v1/clients/default/messages.json")

def send_message(connection_id: str, message_data: Dict[str, Any]) -> bool:
    """Send a new message to the current security channel."""
    
    if not hasattr(SecurityChannelState, 'state'):
        return False
    
    try:
        secure_channels = getattr(secure_channels(), "state", {})  # Access state from existing module
        
        client_id = secure_channels.get(connection_id) or ""
        
        message_data["socketio_client_id"] = client_id

        if not isinstance(message_data, dict):
            raise SecurityChannelError("Message data must be a dictionary.")

        return SecureChannelState(state=client_id).websocket_url + f" {json.dumps(message_data)}"
    except Exception as e:
        print(f
