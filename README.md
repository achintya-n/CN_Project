Project Report: Secure Socket-Based Shopping Application

GITHUB:  https://github.com/achintya-n/CN_Project.git
1. Introduction
This project is a socket programming-based client-server shopping application developed using Python. The primary objective is to demonstrate secure client-server communication, login/signup management, and a basic shopping cart system with GUI interaction using Tkinter. The system uses SSL (Secure Sockets Layer) over raw TCP sockets to ensure encrypted communication, fulfilling the goals of learning practical client-server architecture and secure communication.
________________________________________
2. Features and Architecture
Client-Server Model
The application follows a multi-threaded server architecture using Python's socket, threading, and concurrent.futures.ThreadPoolExecutor. Clients connect securely using SSL sockets. Each client interaction is handled in a separate thread, allowing concurrent sessions.
SSL Encryption
•	SSL is enabled using Python's ssl module.
•	The server loads a certificate (cert.pem) and private key (key.pem) to wrap the socket and ensure encrypted communication.
•	This satisfies the requirement of secure data transfer over raw sockets.
User Authentication
•	Persistent user accounts are stored in users.json.
•	The server supports:
o	SIGNUP – creates a new user
o	LOGIN – authenticates and starts a session
o	LOGOUT – ends the session
Product and Cart System
•	The server hosts a predefined list of products in a dictionary.
•	After login, users can:
o	View products
o	Add items to their cart
o	View cart contents
o	Checkout to place an order and clear the cart
________________________________________
3. GUI Interface (Tkinter)
The client interface is built using Tkinter, offering a user-friendly shopping experience:
•	Authentication screen for login/signup
•	Product display using ttk.Treeview
•	Interactive buttons to add products, view cart, and checkout
•	Message boxes notify users of actions and errors
This GUI enhances the usability of the raw socket-based system and demonstrates front-end and back-end integration.
________________________________________
4. Protocol and Communication
A JSON-based custom protocol is implemented:
•	Every message contains:
o	type: control or data
o	command: indicating the operation (e.g., LOGIN, ADD_CART)
o	Additional fields like username, password, or product_id as needed
•	Responses include status, message, and relevant data
This structured approach ensures clarity and extendibility.
________________________________________
5. Learning Outcomes
•	Implementing SSL over raw sockets
•	Managing concurrent clients with threads
•	Designing a simple yet functional protocol
•	Integrating GUI with backend sockets
•	Real-world understanding of network programming and security
________________________________________
6. Future Improvements
•	Implementing a database (e.g., SQLite) for persistent product/cart storage
•	Adding user session timeout
•	GUI enhancements for a more modern look
•	Adding product images and real-time stock updates
________________________________________
7. Conclusion
This project successfully demonstrates a secure, interactive shopping platform built over raw sockets with SSL encryption and a GUI frontend. It serves as a foundational implementation of client-server architecture, protocol design, and network security principles in real-world applications.
