import socket
import timeit


def measure_tcp_latency(host, port, num_requests):
    latencies = []
    response = ''
    for _ in range(num_requests):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)

            start_time = timeit.default_timer()

            sock.connect((host, port))

            latency = (timeit.default_timer() - start_time) * 1000
            latencies.append(latency)

            sock.close()
        except (socket.timeout, ConnectionRefusedError) as e:
            # print("Error while connecting to server:", e)
            response = f"Error while connecting to server: {e}"
            latencies.append(None)

    valid_latencies = [latency for latency in latencies if latency is not None]

    if valid_latencies:
        avg_latency = sum(valid_latencies) / len(valid_latencies)
        # print(f"Avg Latency for {num_requests} requests: {avg_latency:.4f}")
        response += f"Avg Latency for {num_requests} requests: {avg_latency:.4f} milliseconds.\n"
    else:
        # print("No valid responses found!!")
        response += f"No valid responses found"

    return response
