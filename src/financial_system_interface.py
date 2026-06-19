import socket
import threading

class FinancialSystemInterface:
    def __init__(self):
        self.server_socket = None
        self.clients = []

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
        # Implement the logic to process financial requests
        response = "Request processed successfully"
        return response

if __name__ == "__main__":
    fsi = FinancialSystemInterface()
    fsi.start()
