from math import log

packet_len = 96
line_count = 10001
index = 1

for r in range(1, line_count+1):
	R = f"{str(index).zfill(int(log(line_count+1, 10))+1)} = "
	s = R
	for i in range(1, packet_len - len(R)):
		s += str((len(R) + i) % 10)
	print(s)
