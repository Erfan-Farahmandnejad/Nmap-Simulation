import socket
import threading
import re
from typing import List
import json

HEADER = 128
PORT = 7070
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "DISCONNECT"

# Set up the server socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

USERS = {
    'user1': {'name': 'Alice', 'age': 30},
    'user2': {'name': 'Bob', 'age': 25},
    'user3': {'name': 'Charlie', 'age': 35},
}


# ----------------------------------------------------------------
def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    # Send welcome message and help instructions
    conn.send(
        "Welcome to the Erf Server! I'm here to respond your requests my friend.\nYou can type 'Help' to see the list "
        "of available commands.\n".encode(
            FORMAT))

    connected = True
    while connected:
        try:
            msg_length = conn.recv(HEADER).decode(FORMAT)
            if msg_length:
                msg_length = int(msg_length)
                msg = conn.recv(msg_length).decode(FORMAT)
                if msg == DISCONNECT_MESSAGE:
                    connected = False
                else:
                    print(f"[{addr}] said: {msg}")


        except Exception as e:
            print(f"Error handling message from {addr}: {e}")
            connected = False
    conn.close()
    print(f"[DISCONNECTED] {addr} disconnected.")


# ----------------------------------------------------------------

def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS]: {threading.active_count() - 1}")
        print("[WAITING] waiting for any request...")


print("[STARTING] Server is starting...")
start()
