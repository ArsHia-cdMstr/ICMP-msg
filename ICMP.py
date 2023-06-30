import socket
import time
import struct

def calculate_checksum(data):
    checksum = 0
    for i in range(0, len(data), 2):
        word = (data[i] << 8) + (data[i+1])
        checksum += word
    checksum = (checksum >> 16) + (checksum & 0xffff)
    checksum += (checksum >> 16)
    return ~checksum & 0xffff

def main():
    # Target IP address
    target_ip_address = socket.gethostbyname('google.com')

    print(target_ip_address)
    # Construct the ICMP header
    # B: unsigned char
    # H: unsigned short
    id= 9343
    icmp_header = struct.pack("!BBHHH", 8, 0, 0, id, 1)
    # ICMP data
    icmp_data = b" IM AN ICMP REQUEST :)"
    icmp_packet = icmp_header + icmp_data
    checksum = calculate_checksum(icmp_packet)

    icmp_header = struct.pack("!BBHHH", 8, 0, socket.htons(checksum), id, 1)
    icmp_packet = icmp_header + icmp_data

    print(icmp_packet)

    # Create a socket for sending and receiving ICMP packets
    icmp_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
    icmp_socket.settimeout(2)

    # Send the ICMP packet to the target IP address
    icmp_socket.sendto(icmp_packet, (target_ip_address, 1))

    start_time = time.time()
    try:
        # Receive the response packet
        response_packet, address = icmp_socket.recvfrom(1024)
        print(response_packet)

        # Extract the ICMP type from the response packet
        response_icmp_type = struct.unpack("!B", response_packet[20:21])[0]

        # Check if the response is an ICMP echo reply (type 0)
        if response_icmp_type == 0:
            print(f"ICMP ping to {target_ip_address} successful: {(time.time() - start_time) * 1000}ms ")

    except socket.timeout:
        print(f"No response received from {target_ip_address} within 2 seconds.")
    icmp_socket.close()

if __name__ == "__main__":
    main()
