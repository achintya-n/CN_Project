import socket
import threading
import json
import os
import ssl
from concurrent.futures import ThreadPoolExecutor

# Product inventory
PRODUCTS = {
    "1": {"name": "Laptop", "price": 1000},
    "2": {"name": "Phone", "price": 500},
    "3": {"name": "Headphones", "price": 100},
    "4": {"name": "Mouse", "price": 25},
    "5": {"name": "Keyboard", "price": 45},
    "6": {"name": "Monitor", "price": 150},
    "7": {"name": "Charger", "price": 30},
    "8": {"name": "USB Cable", "price": 10},
    "9": {"name": "Smartwatch", "price": 200},
    "10": {"name": "Tablet", "price": 300},
}

CARTS = {}      # User shopping carts
SESSIONS = {}   # Logged-in sessions

# Load and save users
def load_users():
    if os.path.exists("users.json"):
        with open("users.json", "r") as f:
            return json.load(f)
    return {}

def save_users():
    with open("users.json", "w") as f:
        json.dump(USERS, f)

USERS = load_users()

# Handle a single client connection
def handle_client(client_socket, address):
    print(f"[NEW SSL CONNECTION] {address} connected.")
    user = None

    try:
        while True:
            data = client_socket.recv(2048).decode()
            if not data:
                break
            request = json.loads(data)
            response, user = process_request(request, user)
            client_socket.send(json.dumps(response).encode())
    except (ConnectionResetError, json.JSONDecodeError) as e:
        print(f"[ERROR] {address}: {e}")
    finally:
        if user:
            SESSIONS.pop(user, None)
        client_socket.close()
        print(f"[DISCONNECTED] {address}")

# Process request logic
def process_request(request, user):
    msg_type = request.get("type")
    command = request.get("command")

    if msg_type == "control":
        if command == "SIGNUP":
            username = request["username"]
            password = request["password"]
            if username in USERS:
                return {"status": "error", "message": "Username already exists"}, None
            USERS[username] = password
            CARTS[username] = {}
            save_users()
            return {"status": "success", "message": "Account created"}, None

        if command == "LOGIN":
            username = request["username"]
            password = request["password"]
            if USERS.get(username) == password:
                SESSIONS[username] = True
                if username not in CARTS:
                    CARTS[username] = {}
                return {"status": "success", "message": "Login successful"}, username
            return {"status": "error", "message": "Invalid credentials"}, None

        if command == "LOGOUT":
            if user in SESSIONS:
                del SESSIONS[user]
            return {"status": "success", "message": "Logged out"}, None

    elif msg_type == "data":
        if user is None:
            return {"status": "error", "message": "Login required"}, None

        if command == "GET_PRODUCTS":
            return {"status": "success", "products": PRODUCTS}, user

        elif command == "ADD_CART":
            product_id = request["product_id"]
            if product_id in PRODUCTS:
                cart = CARTS[user]
                if product_id in cart:
                    cart[product_id]["quantity"] += 1
                else:
                    cart[product_id] = {
                        "name": PRODUCTS[product_id]["name"],
                        "price": PRODUCTS[product_id]["price"],
                        "quantity": 1
                    }
                return {"status": "success"}, user
            return {"status": "error", "message": "Invalid product ID"}, user

        elif command == "VIEW_CART":
            return {"status": "success", "cart": list(CARTS[user].values())}, user

        elif command == "CHECKOUT":
            total = sum(item["price"] * item["quantity"] for item in CARTS[user].values())
            CARTS[user].clear()
            return {"status": "success", "message": "Order placed", "total": total}, user

    return {"status": "error", "message": "Invalid request"}, user

# Start server with SSL
def start_server():
    try:
        print("[DEBUG] Creating SSL context...")
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        context.load_cert_chain(certfile="cert.pem", keyfile="key.pem")

        print("[DEBUG] Setting up TCP socket...")
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(("0.0.0.0", 12345))
        server.listen(5)

        print("[SERVER] Listening on port 12345 with SSL")

        with ThreadPoolExecutor(max_workers=10) as executor:
            while True:
                print("[DEBUG] Waiting for a new client to connect...")
                client_socket, addr = server.accept()
                print(f"[NEW CONNECTION] Connection from {addr}")

                ssl_socket = context.wrap_socket(client_socket, server_side=True)
                print(f"[DEBUG] SSL handshake completed with {addr}")

                executor.submit(handle_client, ssl_socket, addr)

    except Exception as e:
        print(f"[FATAL ERROR] Could not start server: {e}")

if __name__ == "__main__":
    start_server(),                                                                                                                             