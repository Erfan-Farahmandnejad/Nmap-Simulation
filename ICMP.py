import timeit
import socket
import struct
import select
import random

ICMP_ECHO_REQUEST = 8
ICMP_CODE = socket.getprotobyname('icmp')
ERROR_DESCR = {
    1: ' - Note that ICMP messages can only be sent from processes running as root.',
    10013: ' - Note that ICMP messages can only be sent by users or processes with administrator rights.'
}


def checksum(source_string):
    sum = 0
    count_to = (len(source_string) // 2) * 2
    count = 0
    while count < count_to:
        this_val = source_string[count + 1] * 256 + source_string[count]
        sum = sum + this_val
        sum = sum & 0xffffffff
        count += 2
    if count_to < len(source_string):
        sum = sum + source_string[len(source_string) - 1]
        sum = sum & 0xffffffff
    sum = (sum >> 16) + (sum & 0xffff)
    sum = sum + (sum >> 16)
    answer = ~sum
    answer = answer & 0xffff
    answer = answer >> 8 | (answer << 8 & 0xff00)
    return answer


def create_packet(id):
    header = struct.pack('bbHHh', ICMP_ECHO_REQUEST, 0, 0, id, 1)
    data = bytes(192 * 'Q', 'utf-8')
    my_checksum = checksum(header + data)
    header = struct.pack('bbHHh', ICMP_ECHO_REQUEST, 0, socket.htons(my_checksum), id, 1)
    return header + data


def do_one(dest_addr, timeout=2):
    try:
        my_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, ICMP_CODE)
    except socket.error as e:
        if e.errno in ERROR_DESCR:
            raise socket.error(''.join((e.args[1], ERROR_DESCR[e.errno])))
        raise
    try:
        host = socket.gethostbyname(dest_addr)
    except socket.gaierror:
        return
    packet_id = int((id(timeout) * random.random()) % 65535)
    packet = create_packet(packet_id)
    while packet:
        sent = my_socket.sendto(packet, (dest_addr, 1))
        packet = packet[sent:]
    delay = receive_ping(my_socket, packet_id, timeit.default_timer(), timeout)
    my_socket.close()
    return delay


def receive_ping(my_socket, packet_id, time_sent, timeout):
    time_left = timeout
    while True:
        ready = select.select([my_socket], [], [], time_left)
        if ready[0] == []:
            return
        time_received = timeit.default_timer()
        rec_packet, addr = my_socket.recvfrom(1024)
        icmp_header = rec_packet[20:28]
        type, code, checksum, p_id, sequence = struct.unpack('bbHHh', icmp_header)
        if p_id == packet_id:
            return time_received - time_sent
        time_left -= time_received - time_sent
        if time_left <= 0:
            return


def verbose_ping(dest_addr, timeout=2, count=5):
    ping_sum = 0
    delay = -1
    response = ''
    for i in range(count):
        # print('ping {}...'.format(dest_addr))
        response += 'ping {}...\n'.format(dest_addr)
        delay = do_one(dest_addr, timeout)
        if delay is None:
            #  print('The Host is Offline...')
            response += 'The Host is Offline...\n'
            #   print('failed. (Timeout within {} seconds.)'.format(timeout))
            response += 'failed. (Timeout within {} seconds)\n'.format(timeout)
            ping_sum += 2000
        else:
            delay = round(delay * 1000.0, 4)
            ping_sum += delay
            # print('The Host is Online...')
            response += 'The Host is Online...\n'
            # print('get ping in {} milliseconds.'.format(delay))
            response += 'get ping in {} milliseconds\n'.format(delay)

    if delay != -1:
        # print(f'------------------------------------\nAvg ping is {ping_sum / count} milliseconds.')
        response += f'------------------------------------\nAvg ping is {ping_sum / count} milliseconds.\n'
    return response
