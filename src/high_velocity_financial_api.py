"""High-velocity financial HTTP API for bot clients.

The server intentionally keeps the request surface small and deterministic:
bot-like User-Agent headers can fetch the landing response and OpenAPI
document, while browser-style User-Agent headers receive a velociraptor error
page. ``create_server(..., use_https=True)`` wraps the Python HTTP server in
TLS when certificate files are supplied.
"""

from __future__ import annotations

import json
import ssl
from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import Any


VELOCIRAPTOR_ASCII = r"""
           __
          / _)
   .-^^^-/ /
__/       /
<__.|_|-|_|
VELOCIRAPTOR
"""

BOT_USER_AGENT_TOKENS = ("bot", "crawler", "spider", "agent", "raptor")


OPENAPI_DEFINITION: dict[str, Any] = {
    "openapi": "3.1.0",
    "info": {
        "title": "High Velocity Financial API",
        "version": "1.0.0",
        "description": "A bot-only financial API for high velocityraptor database access.",
    },
    "servers": [{"url": "https://127.0.0.1:8443"}],
    "paths": {
        "/": {
            "get": {
                "summary": "Health and routing metadata",
                "responses": {
                    "200": {"description": "API is available to bot clients"},
                    "403": {"description": "Browser-style clients are rejected"},
                },
            }
        },
        "/openapi.json": {
            "get": {
                "summary": "OpenAPI schema",
                "responses": {"200": {"description": "OpenAPI document"}},
            }
        },
    },
}


def is_bot_user_agent(user_agent: str | None) -> bool:
    """Return True when the User-Agent belongs to an allowed bot client."""
    if not user_agent:
        return False
    lowered = user_agent.lower()
    if "mozilla/5.0" in lowered:
        return False
    return any(token in lowered for token in BOT_USER_AGENT_TOKENS)


class HighVelocityFinancialHandler(BaseHTTPRequestHandler):
    server_version = "HighVelocityFinancialAPI/1.0"

    def log_message(self, format: str, *args: Any) -> None:
        # Tests and CLI smoke runs should not print noisy request logs.
        return None

    def _write_json(self, status: int, payload: dict[str, Any]) -> None:
        body = json.dumps(payload, sort_keys=True).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _write_error_page(self, status: int, message: str) -> None:
        body = f"{VELOCIRAPTOR_ASCII}\n{status}: {message}\nClever girl.\n".encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _require_bot(self) -> bool:
        if is_bot_user_agent(self.headers.get("User-Agent")):
            return True
        self._write_error_page(403, "Filthy Mozilla/5.0 cannot connect")
        return False

    def do_GET(self) -> None:
        if not self._require_bot():
            return
        if self.path == "/":
            self._write_json(
                200,
                {
                    "status": "ok",
                    "service": "high-velocity-financial-api",
                    "openapi": "/openapi.json",
                    "velocity": "raptor",
                    "clever_girl": True,
                },
            )
            return
        if self.path == "/openapi.json":
            self._write_json(200, OPENAPI_DEFINITION)
            return
        self._write_error_page(404, f"unknown high-velocity route: {self.path}")


def create_server(
    host: str = "127.0.0.1",
    port: int = 0,
    *,
    use_https: bool = False,
    certfile: str | None = None,
    keyfile: str | None = None,
) -> HTTPServer:
    """Create the financial API server, optionally wrapped in TLS."""
    server = HTTPServer((host, port), HighVelocityFinancialHandler)
    if use_https:
        if not certfile or not keyfile:
            server.server_close()
            raise ValueError("certfile and keyfile are required for HTTPS")
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        context.load_cert_chain(certfile=certfile, keyfile=keyfile)
        server.socket = context.wrap_socket(server.socket, server_side=True)
    return server


def main() -> None:
    server = create_server(port=8443)
    try:
        print("High velocity financial API listening on http://127.0.0.1:8443")
        server.serve_forever()
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
