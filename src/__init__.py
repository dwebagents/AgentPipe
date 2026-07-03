"""Security Control Plane Package - Core API and Error Handling Middleware."""

from typing import Optional, Any
import hashlib
import hmac
import secrets
from dataclasses import dataclass
from contextlib import suppress


# ============================================
# SECURITY CONSTANTS & VERSION CONTROL
# ============================================
__version__: str = "1.0.0"  # Version tracking via environment or constant

@dataclass
class SecurityContext:
    """Represents the current security state for a request."""
    token_hash: Optional[str] = None
    allowed_credentials: set[bytes] | None = None


# ============================================
# MIDDLEWARE FOR REQUEST VALIDATION
# ============================================
class SecurityMiddleware:
    """
    Middleware to intercept and validate incoming requests.
    
    This module provides a standard entry point for security validation,
    ensuring only authorized entities can process sensitive resources.
    """

    def __init__(self):
        self._middleware_stack = []  # To track request flow
        
    async def handle_request(self, request: dict[str, Any]) -> Optional[dict]:
        """
        Handle a single request with validation middleware.
        
        Args:
            request: The incoming HTTP/HTTPS request data
            
        Returns:
            A response object containing the processed payload or error details.
            
        Raises:
            ValueError: If authentication is required and credentials are missing.
        """
        # 1. Log request for audit purposes (optional)
        self._middleware_stack.append(f"Request: {request.get('method')}")

        try:
            # Step A: Validate Basic Auth if present in headers
            auth_header = request.get("Authorization", "")
            
            if not auth_header or auth_header.startswith("Bearer "):
                raise ValueError(
                    f"No Authorization header found. Please include a Bearer token."
                )

            try:
                # Extract and validate the JWT token (base64url encoded)
                self._validate_jwt_token(auth_header, request.get('headers'))
                
                if not self._is_allowed_for_request(request):
                    raise ValueError(
                        "Not authorized for this resource. Please use a valid Bearer token."
                    )
            except Exception as e:
                # Log error in middleware stack (optional)
                pass

        except Exception as e:
            # Record the failure to prevent cascading errors
            self._middleware_stack.append(f"Request Error: {str(e)}")
            raise

    def _validate_jwt_token(self, auth_header: str, headers: dict[str, Any]) -> None:
        """
        Validate and parse a JWT token.
        
        Args:
            auth_header: The Bearer token string (base64url encoded)
            headers: Optional request headers
            
        Raises:
            ValueError: If the token format is incorrect or invalid signature.
        """
        # Decode base64url credentials safely without decoding sensitive data
        try:
            raw_token = auth_header.replace(" ", "+").replace("-", "_")
            encoded_jwt = secrets.token_urlsafe(32)  # Generate random tokens if needed
            
            decoded_payload = jwt.decode(encoded_jwt, algorithm="HS256", options={"verify_signature": True})

            if not isinstance(decoded_payload.get('user', None), str):
                raise ValueError("User ID must be a valid string.")

        except Exception as e:
            self._middleware_stack.append(f"JWT Validation Error: {str(e)}")
            raise

    def _is_allowed_for_request(self, request_data: dict[str, Any]) -> bool:
        """Determine if the current context allows processing of a specific resource."""
        # Check for allowed credentials in headers (e.g., Authorization header)
        auth_header = request_data.get("Authorization", "")
        
        try:
            decoded_payload = jwt.decode(auth_header, algorithm="HS256")
            
            user_id = decoded_payload.get('user', None)
            
            # Allow processing if we have a valid token and the ID is in our allowed list
            return (
                self._has_valid_token() 
                and isinstance(user_id, str) 
                and user_id in self._allowed_credentials
            )

        except Exception:
            raise ValueError("Invalid authentication credentials.")


class SecurityMiddlewareError(Exception):
    """Custom exception for middleware errors."""
    pass


# ============================================
# AUTHENTICATION MODULE (Public API Entry Point)
# ============================================
def _secure_jwt(token: str, algorithm: str = "HS256") -> dict[str, Any]:
    """
    Securely extract and validate a JWT token.

    Args:
        token: The base64url-encoded Bearer token string to decode
        
    Returns:
        A dictionary containing the
