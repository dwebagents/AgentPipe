import json

from financial_system_interface import FinancialSystemInterface


def send(interface, payload):
    return json.loads(interface.process_request(json.dumps(payload).encode()))


def test_network_interface_routes_stock_market_requests_without_blanket_success():
    interface = FinancialSystemInterface()

    assert send(interface, {"action": "unknown"})["ok"] is False
    assert send(interface, {"action": "implementation_decision"}) == {
        "ok": True,
        "implementation": "python-domain-layer",
    }

    assert send(interface, {"action": "open_account", "account_id": "issuer"})["ok"] is True
    assert send(interface, {"action": "open_account", "account_id": "investor"})["ok"] is True
    assert send(
        interface, {"action": "deposit", "account_id": "investor", "amount": "100"}
    )["ok"] is True

    ipo = send(
        interface,
        {
            "action": "launch_ipo",
            "symbol": "apip",
            "name": "AgentPipe Inc.",
            "initial_price": "10",
            "shares": 5,
            "treasury_account": "issuer",
        },
    )
    assert ipo["ok"] is True
    assert ipo["symbol"] == "APIP"

    quote = send(interface, {"action": "quote", "symbol": "APIP"})
    assert quote["current_price"] == "10"
    assert quote["available_ipo_shares"] == 5

    updated_quote = send(
        interface,
        {"action": "update_price", "symbol": "APIP", "price": "15"},
    )
    assert updated_quote["current_price"] == "15"
    assert updated_quote["market_cap"] == "75"

    purchase = send(
        interface,
        {
            "action": "buy_ipo_shares",
            "account_id": "investor",
            "symbol": "APIP",
            "shares": 3,
        },
    )
    assert purchase == {"ok": True, "shares": 3, "symbol": "APIP"}

    portfolio = send(interface, {"action": "portfolio_value", "account_id": "investor"})
    assert portfolio == {"account_id": "investor", "market_value": "45", "ok": True}
