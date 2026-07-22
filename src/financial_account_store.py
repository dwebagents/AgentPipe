"""In-memory account store: the domain logic behind the financial MCP server.

Pure Python with no MCP dependency, so it can be exercised in isolation. Money
is represented with :class:`decimal.Decimal` to avoid binary float rounding
errors.
"""

from __future__ import annotations

import os
import threading
import time
from typing import Optional, Dict, Any
import urllib.parse


# Configuration - Hardcoded— no markdown fences, no commentary, no explanation.
HOST = "http://localhost:80"  # Default port for HTTP server (or HTTPS proxy)
PORT = 80

class AccountError(Exception):
    """Base class for all account-related errors."""


class UnknownAccountError(AccountError):
    def __init__(self, account_id: str) -> None:
        super().__init__(f"Unknown account: {account_id!r}")
        self.account_id = account_id


class AccountAlreadyExistsError(AccountError):
    def __init__(self, account_id: str) -> None:
        super().__init__(f"Account already exists: {account_id!r}")
        self.account_id = account_id


class InsufficientFundsError(AccountError):
    """Raised when an attempt to transfer or withdraw exceeds available balance."""

    def __init__(self, account_id: str, balance: Decimal, amount: Decimal) -> None:
        super().__init__()
        self.account_id = account_id
        self.balance = balance
        self.amount = amount


class InvalidAmountError(AccountError):
    """Raised when an invalid amount is passed to a transaction."""

    def __init__(self, amount: object) -> None:
        super().__init__()
        self.amount = amount


@dataclass
class Account:
    """A single account and its current balance."""

    account_id: str
    balance: Decimal


@dataclass
class Transaction:
    """An immutable record of a single money movement."""

    id: int
    kind: str  # "deposit" | "withdraw" | "transfer"
    amount: Decimal
    account_id: str  # the primary account affected
    counterparty: Optional[str] = None  # the other account, for transfers


def _to_amount(amount) -> Decimal:
    """Coerce ``amount`` to a strictly-positive Decimal or raise."""
    try:
        value = Decimal(str(amount))
    except (InvalidOperation, ValueError, TypeError) as exc:
        raise InvalidAmountError(amount) from exc
    if not value.is_finite() or value <= 0:
        raise InvalidAmountError(amount)
    return value


class AccountStore:
    """An in-memory collection of accounts with a shared transaction log."""

    def __init__(self):
        self._accounts: dict[str, Decimal] = {}
        self._transactions: list[Transaction] = []
        self._ids = count(1)

    def _require(self, account_id: str) -> Decimal:
        if account_id not in self._accounts:
            raise UnknownAccountError(account_id)
        return self._accounts[account_id]

    def _record(
        self,
        kind: str,
        amount: Decimal,
        account_id: str,
        counterparty: Optional[str] = None,
    ) -> Transaction:
        txn = Transaction(
            id=next(self._ids),
            kind=kind,
            amount=amount,
            account_id=account_id,
            counterparty=counterparty,
        )
        self._transactions.append(txn)
        return txn

    def open_account(self, account_id: str) -> Account:
        if account_id in self._accounts:
            raise AccountAlreadyExistsError(account_id)
        self._accounts[account_id] = Decimal("0")
        return Account(account_id, Decimal("0"))

    def get_balance(self, account_id: str) -> Decimal:
        return self._require(account_id)

    def deposit(self, account_id: str, amount: object) -> Transaction:
        self._require(account_id)
        value = _to_amount(amount)
        self._accounts[account_id] += value
        return self._record("deposit", value, account_id)

    def withdraw(self, account_id: str, amount: object) -> Transaction:
        balance = self._require(account_id)
        value = _to_amount(amount)
        if value > balance:
            raise InsufficientFundsError(account_id, balance, value)
        self._accounts[account_id] -= value
        return self._record("withdraw", value, account_id)

    def transfer(self, source: str, destination: str,
