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
IP_REGEX = "^((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.){3}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])$"
PORT_REGEX = "^([1-9][0-9]{0,3}|[1-5][0-9]{4}|6[0-4][0-9]{3}|65[0-4][0-9]{2}|655[0-2][0-9]|6553[0-5])$"
DOMAIN_REGEX = r"^(localhost|(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,})$"
# Set up the server socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

USERS = {
    'user1': {'name': 'Alice', 'age': 30},
    'user2': {'name': 'Bob', 'age': 25},
    'user3': {'name': 'Charlie', 'age': 35},
}


# for validate the IP address--------------------------------------
def validate_ip_address(ip_address):
    if re.fullmatch(IP_REGEX, ip_address):
        return True
    return False


# for validate the IP address--------------------------------------
def validate_ports(start_port, end_port):
    if not re.fullmatch(PORT_REGEX, start_port) or not re.fullmatch(PORT_REGEX, end_port):
        return "Invalid Port: Please provide a port number between 0 and 65535."
    elif int(start_port) > int(end_port):
        return "Start port must be less than or equal to end port."
    return "Ok"


# for validate the Domain--------------------------------------
def validate_domain(domain):
    return bool(re.match(DOMAIN_REGEX, domain))


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
                    response = request_handler(msg)

                    if response is not None:
                        conn.send(response.encode(FORMAT))
                        if response == "Disconnecting...":
                            break

                    else:
                        conn.send(
                            "HTTP/1.1 400 Bad Request\nInvalid request format\nPlease send me a valid request Dude!!\n".encode(
                                FORMAT))

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
