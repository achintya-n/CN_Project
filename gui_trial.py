import socket
import json
import tkinter as tk
from tkinter import messagebox, ttk

class ShoppingClient:
    def __init__(self, root):
        self.root = root
        self.root.title("Shop")
        self.root.geometry("500x550")
        self.root.configure(bg="black")

        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect(("127.0.0.1", 12345))

        self.user = None
        self.cart = []

        self.create_auth_screen()

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def send_request(self, request):
        self.client_socket.send(json.dumps(request).encode())
        return json.loads(self.client_socket.recv(2048).decode())

    def create_auth_screen(self):
        self.clear_screen()
        tk.Label(self.root, text="Welcome", font=("Segoe UI", 18), fg="deepskyblue", bg="black").pack(pady=20)
        tk.Button(self.root, text="Login", font=("Segoe UI", 14), bg="blue", fg="white", command=self.create_login_screen).pack(pady=10)
        tk.Button(self.root, text="Sign Up", font=("Segoe UI", 14), bg="green", fg="white", command=self.create_signup_screen).pack(pady=10)

    def create_login_screen(self):
        self.clear_screen()
        tk.Label(self.root, text="Login", font=("Segoe UI", 18), fg="deepskyblue", bg="black").pack(pady=20)
        tk.Label(self.root, text="Username:", font=("Segoe UI", 12), fg="white", bg="black").pack()
        self.username_entry = tk.Entry(self.root, font=("Segoe UI", 12))
        self.username_entry.pack(pady=5)
        tk.Label(self.root, text="Password:", font=("Segoe UI", 12), fg="white", bg="black").pack()
        self.password_entry = tk.Entry(self.root, show="*", font=("Segoe UI", 12))
        self.password_entry.pack(pady=5)
        tk.Button(self.root, text="Login", font=("Segoe UI", 12), bg="blue", fg="white", command=self.login).pack(pady=10)
        tk.Button(self.root, text="Back", font=("Segoe UI", 10), bg="gray", fg="white", command=self.create_auth_screen).pack()

    def create_signup_screen(self):
        self.clear_screen()
        tk.Label(self.root, text="Sign Up", font=("Segoe UI", 18), fg="deepskyblue", bg="black").pack(pady=20)
        tk.Label(self.root, text="Username:", font=("Segoe UI", 12), fg="white", bg="black").pack()
        self.signup_username = tk.Entry(self.root, font=("Segoe UI", 12))
        self.signup_username.pack(pady=5)
        tk.Label(self.root, text="Password:", font=("Segoe UI", 12), fg="white", bg="black").pack()
        self.signup_password = tk.Entry(self.root, show="*", font=("Segoe UI", 12))
        self.signup_password.pack(pady=5)
        tk.Button(self.root, text="Sign Up", font=("Segoe UI", 12), bg="green", fg="white", command=self.signup).pack(pady=10)
        tk.Button(self.root, text="Back", font=("Segoe UI", 10), bg="gray", fg="white", command=self.create_auth_screen).pack()

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        response = self.send_request({"type": "control", "command": "LOGIN", "username": username, "password": password})
        if response["status"] == "success":
            self.user = username
            self.create_main_screen()
        else:
            messagebox.showerror("Login Failed", response["message"])

    def signup(self):
        username = self.signup_username.get()
        password = self.signup_password.get()
        response = self.send_request({"type": "control", "command": "SIGNUP", "username": username, "password": password})
        if response["status"] == "success":
            messagebox.showinfo("Success", response["message"])
            self.create_login_screen()
        else:
            messagebox.showerror("Error", response["message"])

    def logout(self):
        self.send_request({"type": "control", "command": "LOGOUT"})
        self.user = None
        self.create_auth_screen()

    def create_main_screen(self):
        self.clear_screen()
        tk.Label(self.root, text=f"Welcome, {self.user}!", font=("Segoe UI", 14), fg="deepskyblue", bg="black").pack(pady=10)

        self.tree = ttk.Treeview(self.root, columns=("Name", "Price"), show="headings", height=10)
        self.tree.heading("Name", text="Product")
        self.tree.heading("Price", text="Price ($)")
        self.tree.column("Name", anchor="center", width=220)
        self.tree.column("Price", anchor="center", width=100)
        self.tree.pack(pady=10)

        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("Treeview", background="black", fieldbackground="black", foreground="white", rowheight=25, font=("Segoe UI", 10))
        self.style.configure("Treeview.Heading", background="blue", foreground="white", font=("Segoe UI", 11, "bold"))

        self.get_products()

        btn_frame = tk.Frame(self.root, bg="black")
        btn_frame.pack(pady=15)

        tk.Button(btn_frame, text="Add Selected", bg="green", fg="white", font=("Segoe UI", 11), command=self.add_selected).pack(side="left", padx=10)
        tk.Button(btn_frame, text="View Cart", bg="blue", fg="white", font=("Segoe UI", 11), command=self.view_cart).pack(side="left", padx=10)
        tk.Button(btn_frame, text="Logout", bg="red", fg="white", font=("Segoe UI", 11), command=self.logout).pack(side="left", padx=10)

    def get_products(self):
        response = self.send_request({"type": "data", "command": "GET_PRODUCTS"})
        if response["status"] == "success":
            for item_id, item in response["products"].items():
                self.tree.insert("", "end", iid=item_id, values=(item["name"], f"${item['price']}"))

    def add_selected(self):
        selected = self.tree.focus()
        if selected:
            response = self.send_request({"type": "data", "command": "ADD_CART", "product_id": selected})
            if response["status"] == "success":
                messagebox.showinfo("Added", "Product added to cart!")
            else:
                messagebox.showerror("Error", response["message"])
        else:
            messagebox.showwarning("No Selection", "Please select a product.")

    def view_cart(self):
        self.clear_screen()
        tk.Label(self.root, text="Your Cart", font=("Segoe UI", 16), fg="deepskyblue", bg="black").pack(pady=10)
        response = self.send_request({"type": "data", "command": "VIEW_CART"})
        if response["status"] == "success":
            for item in response["cart"]:
                text = f"{item['name']} x{item['quantity']} - ${item['price'] * item['quantity']}"
                tk.Label(self.root, text=text, font=("Segoe UI", 12), fg="white", bg="black").pack()
        tk.Button(self.root, text="Checkout", font=("Segoe UI", 12), bg="green", fg="white", command=self.checkout).pack(pady=10)
        tk.Button(self.root, text="Back", font=("Segoe UI", 11), bg="gray", fg="white", command=self.create_main_screen).pack()

    def checkout(self):
        response = self.send_request({"type": "data", "command": "CHECKOUT"})
        if response["status"] == "success":
            messagebox.showinfo("Order Placed", f"Total: ${response['total']}")
            self.create_main_screen()

def main():
    root = tk.Tk()
    app = ShoppingClient(root)
    root.mainloop()

if __name__ == "__main__":
    main()
