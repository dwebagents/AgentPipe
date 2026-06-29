import json
import socket
import threading

from financial_account_store import AccountError, AccountStore
from stock_market import MarketError, StockMarket


class FinancialSystemInterface:
    def __init__(self):
        self.server_socket = None
        self.clients = []
        self.accounts = AccountStore()
        self.market = StockMarket()

    def start(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(('localhost', 12345))
        self.server_socket.listen(5)

        print("Server started, listening on port 12345")

        while True:
            client_socket, address = self.server_socket.accept()
            print(f"Client connected: {address}")

            threading.Thread(target=self.handle_client, args=(client_socket,)).start()

    def handle_client(self, client_socket):
        try:
            data = client_socket.recv(1024)
            while data:
                print(f"Received from client: {data.decode()}")
                response = self.process_request(data)
                client_socket.sendall(response.encode())
                data = client_socket.recv(1024)
        except Exception as e:
            print(f"Error handling client {client_socket}: {e}")
        finally:
            client_socket.close()
            print(f"Client disconnected: {client_socket}")

    def process_request(self, request):
        try:
            if isinstance(request, bytes):
                request = request.decode()
            payload = json.loads(request)
            action = payload.get("action")

            if action == "open_account":
                account = self.accounts.open_account(payload["account_id"])
                response = {
                    "ok": True,
                    "account_id": account.account_id,
                    "balance": str(account.balance),
                }
            elif action == "deposit":
                txn = self.accounts.deposit(payload["account_id"], payload["amount"])
                response = {
                    "ok": True,
                    "transaction_id": txn.id,
                    "amount": str(txn.amount),
                }
            elif action == "launch_ipo":
                company = self.market.launch_ipo(
                    symbol=payload["symbol"],
                    name=payload["name"],
                    initial_price=payload["initial_price"],
                    shares=payload["shares"],
                    treasury_account=payload["treasury_account"],
                    accounts=self.accounts,
                )
                response = {
                    "ok": True,
                    "symbol": company.symbol,
                    "market_cap": str(company.market_cap),
                }
            elif action == "quote":
                company = self.market.quote(payload["symbol"])
                response = {
                    "ok": True,
                    "symbol": company.symbol,
                    "current_price": str(company.current_price),
                    "available_ipo_shares": company.available_ipo_shares,
                }
            elif action == "update_price":
                company = self.market.update_price(payload["symbol"], payload["price"])
                response = {
                    "ok": True,
                    "symbol": company.symbol,
                    "current_price": str(company.current_price),
                    "market_cap": str(company.market_cap),
                }
            elif action == "buy_ipo_shares":
                purchase = self.market.buy_ipo_shares(
                    account_id=payload["account_id"],
                    symbol=payload["symbol"],
                    shares=payload["shares"],
                    accounts=self.accounts,
                )
                response = {
                    "ok": True,
                    "symbol": purchase.symbol,
                    "shares": purchase.shares,
                }
            elif action == "portfolio_value":
                response = {
                    "ok": True,
                    "account_id": payload["account_id"],
                    "market_value": str(
                        self.market.portfolio_value(payload["account_id"])
                    ),
                }
            elif action == "linkedin_milestone_post":
                response = {
                    "ok": True,
                    "post": self.market.linkedin_milestone_post(payload["account_id"]),
                }
            elif action == "implementation_decision":
                response = {"ok": True, "implementation": self.market.implementation_decision}
            else:
                response = {"ok": False, "error": f"unknown action: {action!r}"}
        except (KeyError, json.JSONDecodeError, AccountError, MarketError, ValueError) as exc:
            response = {"ok": False, "error": str(exc)}
        return json.dumps(response, sort_keys=True)

if __name__ == "__main__":
    fsi = FinancialSystemInterface()
    fsi.start()
