import os
import math
import sys

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

print(f"{file1}: {file1_size} bytes")
print(f"{file2}: {file2_size} bytes")

min_file_size = min(file1_size, file2_size)
bit_difference_count = 0

with open(file1, 'rb') as f1:
    with open(file2, 'rb') as f2:
        read_bytes = 0
        while read_bytes < min_file_size:
            b1 = ord(f1.read(1))
            b2 = ord(f2.read(1))
            bit_diff = bit_difference(b1, b2)
            read_bytes += 1
            bit_difference_count += bit_diff

ber = bit_difference_count / (read_bytes * 8)
print(f"Bit Error Rate: {ber} -> {bit_difference_count} different bits in {read_bytes} bytes ({read_bytes * 8} bits).")