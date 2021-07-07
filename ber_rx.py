import os
import math
import sys
import struct

def bit_difference(b1, b2):
    xor = b1 ^ b2
    diff = 0
    while xor:
        xor = xor & (xor - 1)
        diff += 1
    return diff

if len(sys.argv[1:]) != 2:
    print("File path or file paths missing.")
    sys.exit()
else:
    exit = False

    if not os.path.isfile(sys.argv[1]):
        print(f"File does not exist in path: '{sys.argv[1]}'")
        exit = True
    if not os.path.isfile(sys.argv[2]):
        print(f"File does not exist in path: '{sys.argv[2]}'")
        exit = True
    if exit:
        sys.exit()

file1 = sys.argv[1]
file2 = sys.argv[2]

file1_size = os.stat(file1).st_size
file2_size = os.path.getsize(file2)

# print(f"Packet from {file1}: {file1_size} bytes")
# print(f"Received packets from {file2}: {file2_size} bytes")
packet_len = 96
packet = []

with open(file1, 'rb') as f1:
    read_bytes = 0
    while read_bytes < packet_len:
        # b1, = struct.unpack('b', f1.read(1))
        b1 = ord(f1.read(1))
        packet.append(b1)
        read_bytes += 1

bit_difference_count = 0

with open(file2, 'rb') as f2:
    read_bytes = 0
    while read_bytes < file2_size:
        b2 = ord(f2.read(1))
        bit_diff = bit_difference(b2, packet[read_bytes % packet_len])
        read_bytes += 1
        bit_difference_count += bit_diff

ber = bit_difference_count / (read_bytes * 8)
print(f"Bit Error Rate in Received Packets: {ber} -> {bit_difference_count} different bits in {read_bytes * 8} bits ({read_bytes/packet_len} packets).")

transmission_count = 10000
total_transmitted_bytes = packet_len * transmission_count
not_received_bytes = total_transmitted_bytes - read_bytes
not_received_bits = not_received_bytes * 8
total_ber = (bit_difference_count + not_received_bits) / (total_transmitted_bytes * 8)
print(f"Total Bit Error Rate: {total_ber} -> {bit_difference_count} different bits, {not_received_bytes/packet_len} not received packets in {total_transmitted_bytes * 8} bits ({total_transmitted_bytes/packet_len} packets).")

print(f"BER: {ber:.10f}, Undetected Packet Count: {not_received_bytes//packet_len}")