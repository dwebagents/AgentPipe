"""Smoke tests for the financial MCP server adapter.

These drive the FastMCP server in-memory (no stdio transport) to confirm the
tools are registered and round-trip through the underlying AccountStore.
"""

import asyncio
import json

import pytest
from mcp.server.fastmcp.exceptions import ToolError

import financial_mcp_server as srv

EXPECTED_TOOLS = {
    "open_account",
    "get_balance",
    "deposit",
    "withdraw",
    "transfer",
    "list_transactions",
    "launch_ipo",
    "get_stock_quote",
    "update_stock_price",
    "buy_ipo_shares",
    "get_portfolio_value",
    "linkedin_milestone_post",
}


def _run(coro):
    return asyncio.run(coro)


def _payload(result):
    """Extract the JSON payload from a FastMCP call_tool result.

    FastMCP returns either a ``(content, structured)`` tuple (scalar returns) or
    a plain content list (dict/list returns serialized to JSON text). Normalize
    both to the decoded Python object.
    """
    if isinstance(result, tuple):
        return result[1]
    return json.loads(result[0].text)


def setup_function(_func):
    # Reset the module-level store so each test starts from a clean slate.
    srv._store.__init__()
    srv._market.__init__()


def test_expected_tools_are_registered():
    tools = _run(srv.mcp.list_tools())
    names = {tool.name for tool in tools}
    assert EXPECTED_TOOLS <= names


def test_open_deposit_balance_roundtrip():
    _run(srv.mcp.call_tool("open_account", {"account_id": "alice"}))
    _run(srv.mcp.call_tool("deposit", {"account_id": "alice", "amount": "100.50"}))
    balance = _payload(_run(srv.mcp.call_tool("get_balance", {"account_id": "alice"})))
    assert balance["account_id"] == "alice"
    assert balance["balance"] == "100.50"


def test_transfer_between_accounts():
    _run(srv.mcp.call_tool("open_account", {"account_id": "alice"}))
    _run(srv.mcp.call_tool("open_account", {"account_id": "bob"}))
    _run(srv.mcp.call_tool("deposit", {"account_id": "alice", "amount": "100"}))
    _run(
        srv.mcp.call_tool(
            "transfer", {"source": "alice", "destination": "bob", "amount": "30"}
        )
    )
    alice = _payload(_run(srv.mcp.call_tool("get_balance", {"account_id": "alice"})))
    bob = _payload(_run(srv.mcp.call_tool("get_balance", {"account_id": "bob"})))
    assert alice["balance"] == "70"
    assert bob["balance"] == "30"


def test_domain_error_surfaces_as_tool_error():
    with pytest.raises(ToolError):
        _run(srv.mcp.call_tool("get_balance", {"account_id": "ghost"}))


def test_stock_market_ipo_roundtrip_through_mcp_tools():
    _run(srv.mcp.call_tool("open_account", {"account_id": "issuer"}))
    _run(srv.mcp.call_tool("open_account", {"account_id": "investor"}))
    _run(srv.mcp.call_tool("deposit", {"account_id": "investor", "amount": "250"}))

    ipo = _payload(
        _run(
            srv.mcp.call_tool(
                "launch_ipo",
                {
                    "symbol": "apip",
                    "name": "AgentPipe Inc.",
                    "initial_price": "25",
                    "shares": 10,
                    "treasury_account": "issuer",
                },
            )
        )
    )
    assert ipo["symbol"] == "APIP"
    assert ipo["market_cap"] == "250"

    purchase = _payload(
        _run(
            srv.mcp.call_tool(
                "buy_ipo_shares",
                {"account_id": "investor", "symbol": "APIP", "shares": 4},
            )
        )
    )
    assert purchase["gross_amount"] == "100"

    portfolio = _payload(
        _run(srv.mcp.call_tool("get_portfolio_value", {"account_id": "investor"}))
    )
    assert portfolio["market_value"] == "100"
    assert portfolio["holdings"] == [
        {"symbol": "APIP", "shares": 4, "market_value": "100"}
    ]
