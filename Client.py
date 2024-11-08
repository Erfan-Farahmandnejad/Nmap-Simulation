import json
import socket
import re
import threading

HEADER = 128
PORT = 7070
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "DISCONNECT"
SERVER = "192.168.21.1"
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)


# Function to handle sending messages
def send_message():
    while True:
        msg = input()
        if msg == DISCONNECT_MESSAGE:
            send(msg)
            print("Disconnected from server!!")
            client.close()
            break
        else:
            send(msg)


# Function to handle receiving messages
def receive_message():
    while True:
        try:
            message = client.recv(2048).decode(FORMAT)
            if message:
                try:
                    response = json.loads(message)
                    print(
                        f"Server:\n{response}----------------------------------------------------\nYour next "
                        f"request?...\n")
                except json.JSONDecodeError:
                    print(message)
            else:
                print("Disconnected from server.")
                break
        except ConnectionResetError:
            print("Server connection was closed.")
            break


# Helper function to format and send messages
def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)


# Starting threads for reading and writing
receive_thread = threading.Thread(target=receive_message)
send_thread = threading.Thread(target=send_message)

receive_thread.start()
send_thread.start()

# Wait for threads to complete before exiting
receive_thread.join()
send_thread.join()
