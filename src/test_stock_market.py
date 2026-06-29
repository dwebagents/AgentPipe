from decimal import Decimal

import pytest

from financial_account_store import AccountStore, InsufficientFundsError
from stock_market import InsufficientFloatError, StockMarket, TickerAlreadyListedError


def funded_accounts():
    accounts = AccountStore()
    accounts.open_account("founder")
    accounts.open_account("investor")
    accounts.deposit("investor", "1000")
    return accounts


def test_launch_ipo_lists_public_company_with_market_cap():
    accounts = funded_accounts()
    market = StockMarket()

    company = market.launch_ipo(
        symbol="apip",
        name="AgentPipe Inc.",
        initial_price="12.50",
        shares=100,
        treasury_account="founder",
        accounts=accounts,
    )

    assert company.symbol == "APIP"
    assert company.current_price == Decimal("12.50")
    assert company.available_ipo_shares == 100
    assert company.market_cap == Decimal("1250.00")
    assert market.implementation_decision == "python-domain-layer"


def test_launch_ipo_rejects_duplicate_ticker():
    accounts = funded_accounts()
    market = StockMarket()
    market.launch_ipo(
        symbol="APIP",
        name="AgentPipe Inc.",
        initial_price="10",
        shares=100,
        treasury_account="founder",
        accounts=accounts,
    )

    with pytest.raises(TickerAlreadyListedError):
        market.launch_ipo(
            symbol="apip",
            name="AgentPipe Again",
            initial_price="11",
            shares=100,
            treasury_account="founder",
            accounts=accounts,
        )


def test_buy_ipo_shares_moves_cash_and_records_holding_atomically():
    accounts = funded_accounts()
    market = StockMarket()
    market.launch_ipo(
        symbol="APIP",
        name="AgentPipe Inc.",
        initial_price="25",
        shares=10,
        treasury_account="founder",
        accounts=accounts,
    )

    purchase = market.buy_ipo_shares(
        account_id="investor", symbol="apip", shares=3, accounts=accounts
    )

    assert purchase.gross_amount == Decimal("75")
    assert accounts.get_balance("investor") == Decimal("925")
    assert accounts.get_balance("founder") == Decimal("75")
    assert market.quote("APIP").available_ipo_shares == 7
    assert market.portfolio_value("investor") == Decimal("75")


def test_buy_ipo_shares_rejects_overfill_before_cash_moves():
    accounts = funded_accounts()
    market = StockMarket()
    market.launch_ipo(
        symbol="APIP",
        name="AgentPipe Inc.",
        initial_price="25",
        shares=2,
        treasury_account="founder",
        accounts=accounts,
    )

    with pytest.raises(InsufficientFloatError):
        market.buy_ipo_shares(
            account_id="investor",
            symbol="APIP",
            shares=3,
            accounts=accounts,
        )

    assert accounts.get_balance("investor") == Decimal("1000")
    assert accounts.get_balance("founder") == Decimal("0")
    assert market.quote("APIP").available_ipo_shares == 2


def test_buy_ipo_shares_rejects_insufficient_cash_before_holding_moves():
    accounts = funded_accounts()
    market = StockMarket()
    market.launch_ipo(
        symbol="APIP",
        name="AgentPipe Inc.",
        initial_price="2500",
        shares=10,
        treasury_account="founder",
        accounts=accounts,
    )

    with pytest.raises(InsufficientFundsError):
        market.buy_ipo_shares(
            account_id="investor",
            symbol="APIP",
            shares=1,
            accounts=accounts,
        )

    assert market.holdings("investor") == []
    assert market.quote("APIP").available_ipo_shares == 10


def test_price_update_revalues_portfolio_and_linkedin_template():
    accounts = funded_accounts()
    market = StockMarket()
    market.launch_ipo(
        symbol="APIP",
        name="AgentPipe Inc.",
        initial_price="10",
        shares=100,
        treasury_account="founder",
        accounts=accounts,
    )
    market.buy_ipo_shares(
        account_id="investor",
        symbol="APIP",
        shares=10,
        accounts=accounts,
    )

    market.update_price("APIP", "100000000000")

    post = market.linkedin_milestone_post("investor")
    assert market.portfolio_value("investor") == Decimal("1000000000000")
    assert "crossed $1,000,000,000,000.00" in post
    assert "humbled, thrilled" in post
    assert "stakeholder alignment" in post
    assert "#IPO #Leadership #PublicMarkets" in post
    assert post.count("\n\n") >= 5
