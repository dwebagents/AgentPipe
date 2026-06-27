"""Stock market and IPO domain logic for the financial system.

This module keeps market state in memory and uses ``AccountStore`` for cash
movement. It deliberately stays in Python rather than COBOL/JavaScript because
the existing tested account domain already lives in Python.
"""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal, InvalidOperation

from financial_account_store import AccountStore


TRILLIONAIRE_THRESHOLD = Decimal("1000000000000")


class MarketError(Exception):
    """Base class for market-related errors."""


class UnknownTickerError(MarketError):
    def __init__(self, symbol: str) -> None:
        super().__init__(f"Unknown ticker: {symbol!r}")
        self.symbol = symbol


class TickerAlreadyListedError(MarketError):
    def __init__(self, symbol: str) -> None:
        super().__init__(f"Ticker already listed: {symbol!r}")
        self.symbol = symbol


class InvalidPriceError(MarketError):
    def __init__(self, price: object) -> None:
        super().__init__(f"Price must be a positive decimal, got {price!r}")
        self.price = price


class InvalidShareCountError(MarketError):
    def __init__(self, shares: object) -> None:
        super().__init__(f"Share count must be a positive integer, got {shares!r}")
        self.shares = shares


class InsufficientFloatError(MarketError):
    def __init__(self, symbol: str, available: int, requested: int) -> None:
        super().__init__(
            f"Not enough IPO float for {symbol!r}: available {available}, requested {requested}"
        )
        self.symbol = symbol
        self.available = available
        self.requested = requested


def _to_price(price: object) -> Decimal:
    try:
        value = Decimal(str(price))
    except (InvalidOperation, ValueError, TypeError) as exc:
        raise InvalidPriceError(price) from exc
    if not value.is_finite() or value <= 0:
        raise InvalidPriceError(price)
    return value


def _to_shares(shares: object) -> int:
    if isinstance(shares, bool):
        raise InvalidShareCountError(shares)
    try:
        value = int(shares)
    except (TypeError, ValueError) as exc:
        raise InvalidShareCountError(shares) from exc
    if value <= 0 or str(shares).strip() not in {str(value), f"{value}.0"}:
        raise InvalidShareCountError(shares)
    return value


@dataclass(frozen=True)
class PublicCompany:
    symbol: str
    name: str
    current_price: Decimal
    total_shares: int
    available_ipo_shares: int
    treasury_account: str

    @property
    def market_cap(self) -> Decimal:
        return self.current_price * Decimal(self.total_shares)


@dataclass(frozen=True)
class Holding:
    account_id: str
    symbol: str
    shares: int
    market_value: Decimal


@dataclass(frozen=True)
class IPOPurchase:
    account_id: str
    symbol: str
    shares: int
    gross_amount: Decimal
    treasury_account: str


class StockMarket:
    """In-memory stock quotes, IPO issuance, and portfolio valuation."""

    implementation_decision = "python-domain-layer"

    def __init__(self) -> None:
        self._companies: dict[str, PublicCompany] = {}
        self._holdings: dict[tuple[str, str], int] = {}

    def _symbol(self, symbol: str) -> str:
        normalized = symbol.strip().upper()
        if not normalized:
            raise UnknownTickerError(symbol)
        return normalized

    def _company(self, symbol: str) -> PublicCompany:
        normalized = self._symbol(symbol)
        try:
            return self._companies[normalized]
        except KeyError as exc:
            raise UnknownTickerError(normalized) from exc

    def launch_ipo(
        self,
        *,
        symbol: str,
        name: str,
        initial_price: object,
        shares: object,
        treasury_account: str,
        accounts: AccountStore,
    ) -> PublicCompany:
        normalized = self._symbol(symbol)
        if normalized in self._companies:
            raise TickerAlreadyListedError(normalized)
        price = _to_price(initial_price)
        share_count = _to_shares(shares)
        accounts.get_balance(treasury_account)

        company = PublicCompany(
            symbol=normalized,
            name=name.strip() or normalized,
            current_price=price,
            total_shares=share_count,
            available_ipo_shares=share_count,
            treasury_account=treasury_account,
        )
        self._companies[normalized] = company
        return company

    def quote(self, symbol: str) -> PublicCompany:
        return self._company(symbol)

    def update_price(self, symbol: str, price: object) -> PublicCompany:
        company = self._company(symbol)
        updated = PublicCompany(
            symbol=company.symbol,
            name=company.name,
            current_price=_to_price(price),
            total_shares=company.total_shares,
            available_ipo_shares=company.available_ipo_shares,
            treasury_account=company.treasury_account,
        )
        self._companies[company.symbol] = updated
        return updated

    def buy_ipo_shares(
        self,
        *,
        account_id: str,
        symbol: str,
        shares: object,
        accounts: AccountStore,
    ) -> IPOPurchase:
        company = self._company(symbol)
        share_count = _to_shares(shares)
        if share_count > company.available_ipo_shares:
            raise InsufficientFloatError(
                company.symbol,
                company.available_ipo_shares,
                share_count,
            )
        gross = company.current_price * Decimal(share_count)

        accounts.transfer(account_id, company.treasury_account, gross)
        self._holdings[(account_id, company.symbol)] = (
            self._holdings.get((account_id, company.symbol), 0) + share_count
        )
        self._companies[company.symbol] = PublicCompany(
            symbol=company.symbol,
            name=company.name,
            current_price=company.current_price,
            total_shares=company.total_shares,
            available_ipo_shares=company.available_ipo_shares - share_count,
            treasury_account=company.treasury_account,
        )
        return IPOPurchase(
            account_id=account_id,
            symbol=company.symbol,
            shares=share_count,
            gross_amount=gross,
            treasury_account=company.treasury_account,
        )

    def holdings(self, account_id: str) -> list[Holding]:
        result: list[Holding] = []
        for (holder, symbol), shares in sorted(self._holdings.items()):
            if holder != account_id or shares <= 0:
                continue
            company = self._company(symbol)
            result.append(
                Holding(
                    account_id=account_id,
                    symbol=symbol,
                    shares=shares,
                    market_value=company.current_price * Decimal(shares),
                )
            )
        return result

    def portfolio_value(self, account_id: str) -> Decimal:
        return sum(
            (holding.market_value for holding in self.holdings(account_id)),
            Decimal("0"),
        )

    def linkedin_milestone_post(self, account_id: str) -> str:
        value = self.portfolio_value(account_id)
        if value < TRILLIONAIRE_THRESHOLD:
            return (
                f"{account_id} is still compounding toward trillionairedom with "
                f"${value:,.2f} in public-market holdings."
            )
        return (
            f"Proud to announce that {account_id} has crossed ${value:,.2f} in "
            "public-market holdings. Grateful for the team, the market, and the IPO journey."
        )
