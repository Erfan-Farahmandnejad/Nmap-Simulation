# Nmap-Simulation: Network Scanning & Diagnostics Tool ⚡

## 🌟 Overview
This project is a **Python-based Nmap-Simulation** that mimics the functionality of **Nmap**, allowing users to perform **network scanning, real-time messaging, and diagnostics**. The system includes a **central server** managing multiple clients, supports **TCP/IP communication**, and provides **ICMP functionalities** for analyzing network performance.

---

## 🚀 Features
✅ **Network Scanning**: Simulates Nmap by scanning open ports and detecting active hosts 📡.  
✅ **Client-Server Communication**: Enables clients to connect to a server for exchanging messages 🔄.  
✅ **Multi-Client Handling**: Supports multiple simultaneous client connections ⚡.  
✅ **ICMP Support**: Provides network diagnostics and latency checks using ICMP 📶.  
✅ **TCP Latency Measurement**: Measures response times of network devices ⏳.  
✅ **Real-Time Data Transfer**: Facilitates instant communication and packet analysis 💬.  


---

## 📂 File Structure
```
Nmap-Simulation/
│── Server.py          # Main server script handling network connections and scanning
│── Client.py          # Client script for interacting with the network scanner
│── ICMP.py            # Implements ICMP-based diagnostics and host discovery
│── TCP_Latency.py     # Measures response times of network devices
│── README.md          # Project documentation
```

---

## 🔧 Installation & Setup

### **1️⃣ Prerequisites**
Ensure you have **Python 3.x** installed.

### **2️⃣ Clone the Repository**
```sh
git clone https://github.com/Erfan-fn/Nmap-Simulation.git
cd Nmap-Simulation
```

### **3️⃣ Running the Scripts**

#### **Starting the Server**
```sh
python Server.py
```

#### **Starting the Client**
```sh
python Client.py
```

#### **Performing ICMP Network Analysis**
```sh
python ICMP.py
```

#### **Measuring TCP Latency**
```sh
python TCP_Latency.py
```

---

## 📡 Project Functions

### **Server Functions (Server.py)**
- `start_server(port)`: Initializes and starts the server to listen for client connections.
- `handle_client(client_socket, address)`: Manages client communication and processes requests.
- `scan_ports(target_ip, port_range)`: Scans specified ports on a target machine to detect open services.

### **Client Functions (Client.py)**
- `connect_to_server(server_ip, port)`: Establishes a connection between the client and the server.
- `send_message(message)`: Sends a message from the client to the server.
- `receive_response()`: Receives responses from the server after sending a request.

### **ICMP Functions (ICMP.py)**
- `send_icmp_echo_request(target_ip)`: Sends an ICMP Echo Request to the target IP to check if it is reachable.
- `receive_icmp_reply(timeout=2)`: Waits for an ICMP Echo Reply within the specified timeout.
- `measure_latency(target_ip)`: Measures the round-trip time (RTT) of packets sent to the target.
- `analyze_packet_loss(target_ip, count=5)`: Sends multiple ICMP requests and calculates packet loss percentage.
- `trace_route(target_ip, max_hops=30)`: Determines the path taken by packets to reach the target by incrementing the TTL value.

### **TCP Latency Functions (TCP_Latency.py)**
- `measure_tcp_latency(target_ip, port)`: Measures the response time of a target server on a given port.
- `analyze_network_performance(target_ip, port_range)`: Evaluates network performance by checking multiple ports.

---

## 📜 License
This project is licensed under the **MIT License**. See [LICENSE](LICENSE) for details.


