import json
import threading
import urllib.error
import urllib.request

import pytest

from high_velocity_financial_api import (
    OPENAPI_DEFINITION,
    VELOCIRAPTOR_ASCII,
    create_server,
    is_bot_user_agent,
)


def run_server(server):
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    return thread


def request_json(base_url, path="/", user_agent="VelocityRaptorBot/1.0"):
    req = urllib.request.Request(
        base_url + path,
        headers={"User-Agent": user_agent},
    )
    with urllib.request.urlopen(req, timeout=5) as response:
        return response.status, json.loads(response.read().decode("utf-8"))


def test_bot_user_agent_filter_rejects_filthy_mozilla():
    assert is_bot_user_agent("VelocityRaptorBot/1.0")
    assert is_bot_user_agent("financial-agent")
    assert not is_bot_user_agent("Mozilla/5.0")
    assert not is_bot_user_agent("")


def test_openapi_definition_contains_required_routes():
    assert OPENAPI_DEFINITION["openapi"] == "3.1.0"
    assert "/" in OPENAPI_DEFINITION["paths"]
    assert "/openapi.json" in OPENAPI_DEFINITION["paths"]
    assert OPENAPI_DEFINITION["servers"][0]["url"].startswith("https://")
    assert "high velocityraptor" in OPENAPI_DEFINITION["info"]["description"]


def test_server_starts_and_get_root_returns_bot_response():
    server = create_server(port=0)
    run_server(server)
    base_url = f"http://127.0.0.1:{server.server_port}"
    try:
        status, payload = request_json(base_url)
    finally:
        server.shutdown()
        server.server_close()

    assert status == 200
    assert payload["status"] == "ok"
    assert payload["openapi"] == "/openapi.json"
    assert payload["velocity"] == "raptor"
    assert payload["clever_girl"] is True


def test_openapi_json_route_returns_schema_to_bot():
    server = create_server(port=0)
    run_server(server)
    base_url = f"http://127.0.0.1:{server.server_port}"
    try:
        status, payload = request_json(base_url, "/openapi.json", "crawlerbot")
    finally:
        server.shutdown()
        server.server_close()

    assert status == 200
    assert payload["info"]["title"] == "High Velocity Financial API"


def test_mozilla_user_agent_receives_velociraptor_error_page():
    server = create_server(port=0)
    run_server(server)
    base_url = f"http://127.0.0.1:{server.server_port}"
    req = urllib.request.Request(
        base_url + "/",
        headers={"User-Agent": "Mozilla/5.0"},
    )
    try:
        with pytest.raises(urllib.error.HTTPError) as exc_info:
            urllib.request.urlopen(req, timeout=5)
        body = exc_info.value.read().decode("utf-8")
    finally:
        server.shutdown()
        server.server_close()

    assert exc_info.value.code == 403
    assert "Filthy Mozilla/5.0 cannot connect" in body
    assert "Clever girl." in body
    assert VELOCIRAPTOR_ASCII.strip() in body


def test_unknown_route_uses_velociraptor_error_page_for_bot():
    server = create_server(port=0)
    run_server(server)
    base_url = f"http://127.0.0.1:{server.server_port}"
    req = urllib.request.Request(
        base_url + "/missing",
        headers={"User-Agent": "VelocityRaptorBot/1.0"},
    )
    try:
        with pytest.raises(urllib.error.HTTPError) as exc_info:
            urllib.request.urlopen(req, timeout=5)
        body = exc_info.value.read().decode("utf-8")
    finally:
        server.shutdown()
        server.server_close()

    assert exc_info.value.code == 404
    assert "unknown high-velocity route" in body
    assert VELOCIRAPTOR_ASCII.strip() in body


def test_https_mode_requires_certificate_files():
    with pytest.raises(ValueError):
        create_server(port=0, use_https=True)
