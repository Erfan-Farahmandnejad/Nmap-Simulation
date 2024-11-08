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


# for validate the Domain------------------------------------------
def validate_domain(domain):
    return bool(re.match(DOMAIN_REGEX, domain))


# check ports status-----------------------------------------------

def check_ports(ip, start_port, end_port, timeout=3):
    results = {}
    temp = ''
    ip_status = ICMP.verbose_ping(ip, 2, 1)
    if ip_status.__contains__("Offline"):
        ip_status = "Offline"
    else:
        ip_status = "Online"

    try:
        # Attempt to resolve hostname, default to IP if fails------
        hostname = socket.gethostbyaddr(ip)[0]
    except (socket.herror, socket.gaierror):
        hostname = ip
        # check status of all ports in range-----------------------
    for port in range(start_port, end_port + 1):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        try:
            sock.connect((ip, port))

            results[
                port] = f"-- Port: {port}    -- Status: Open    -- Service: {show_service(port)}    -- Hostname: {hostname}"
            temp += f"-- Port: {port}    -- Status: Open    -- Service: {show_service(port)}    -- Hostname: {hostname}\n"

        except (socket.timeout, ConnectionRefusedError):
            # Mark as closed if connection fails-------------------
            results[
                port] = f"-- Port: {port}    -- Status: Closed    -- Service: {show_service(port)}    -- Hostname: {hostname}"
            temp += f"-- Port: {port}    -- Status: Closed    -- Service:  {show_service(port)}   -- Hostname: {hostname}\n"
        except Exception as e:
            # Handle unexpected errors-----------------------------
            results[
                port] = f"-- Port: {port}    -- Status: Error: {e}    -- Service: {show_service(port)}    -- Hostname: {hostname}"
            temp += f"-- Port: {port}    -- Status: Error: {e}    -- Service: {show_service(port)}    -- Hostname: {hostname}\n"

    # Add IP status------------------------------------------------
    response = f"{ip} is {ip_status}\n" + temp
    return response


# ----show service-------------------------------------------------
def show_service(port, protocol='tcp'):
    try:
        service_name = socket.getservbyport(port, protocol)
        return f"Service name: {service_name}"
    except OSError:
        return "Unknown service"


# Get--------------------------------------------------------------

def handle_get_request(request):
    request_parts = request.split()
    if len(request_parts) >= 2:
        user_id = request_parts[1]
        if f'user{user_id}' in USERS.keys():
            user_info = USERS[f'user{user_id}']
            response = f"HTTP/1.1 200 OK\nContent-Type: application/json\n\n{json.dumps(user_info)}"
        else:
            response = "HTTP/1.1 404 Not Found\nUser not found"
    else:
        response = "HTTP/1.1 400 Bad Request\nInvalid request format."
    return response


# Post-------------------------------------------------------------
def handle_post_request(request):
    command = request.split()
    if len(command) >= 3:
        name = command[1]
        age = command[2]
        if age.isdigit():
            new_user_id = f'user{len(USERS) + 1}'
            USERS[new_user_id] = {'name': name, 'age': int(age)}
            response = "HTTP/1.1 200 OK\nUser data updated"
        else:
            response = "HTTP/1.1 400 Bad Request\nInvalid age format."
    else:
        response = "HTTP/1.1 400 Bad Request\nInvalid request format."
    return response


# Help-------------------------------------------------------------

def help_request():
    help_text = """
    Here are the available commands:

    1. **Get User Information**
       Format: Get <user_id>
       Example: Get 1
       Description: Retrieves information of the user with the specified user_id.

    2. **Post User Data**
       Format: Post <name> <age>
       Example: Post John 28
       Description: Adds a new user with the specified name and age.

    3. **Ping IP Address**
       Format: Ping <ip_address> <timeout> <count>
       Example: Ping 192.168.1.1 2 5
       Description: Pings the IP address with optional timeout and count.

    4. **Check Port Range**
       Format: Check <ip_address> <start_port> <end_port>
       Example: Check 192.168.1.1 80 100
       Description: Checks the status of ports in the specified range on the IP.

    5. **Measure Latency**
       Format: Latency <ip_address> <port> <num_requests>
       Example: Latency 192.168.1.1 80 10
       Description: Measures the TCP latency to a specific IP and port.

    6. **Disconnect**
       Format: DISCONNECT
       Description: Disconnects from the server.

    Type 'Help' to view this information again at any time.
    """
    return help_text


# function for handle communication between clients----------------
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


# -----------------------------------------------------------------

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
