# Start A5.1
# Start A5.2
# Start A5.3
# Start A5.4

import json
import struct
import sys  # Nur für A5.2 und A5.4


def parse_udp_packet(packet: bytes) -> (int, int, int, int, bytes):
    end = len(packet)
    return int.from_bytes(packet[0:2], "big"), int.from_bytes(packet[2:4], "big"), \
           int.from_bytes(packet[4:6], "big"), int.from_bytes(packet[6:8], "big"), packet[8:end]


# End A5.1

# Uncomment for pasting
"""
try:
    path = sys.argv[1]
except IndexError as ie:
    print("Please give an argument.\nRunning with args[1] = \"example_packet\"")
    path = "example_packet"

file = open(path, "rb")
content = file.read()
file.close()
port_from, port_to, length, checksum, data = parse_udp_packet(content)
print("UDP datagram from: " + str(port_from) + "\nto: " + str(port_to) + "\nlength: " + str(length) + "\nchecksum: " + str(checksum) + "\ndata: " + data.hex())
"""


# End A5.2


def build_udp_packet(source_port: int, destination_port: int, data: bytes) -> bytes:
    length = 8 + len(data)
    obj = struct.pack("!HHHH" + str(len(data)) + "s", source_port, destination_port, length, 0, data)
    return obj


# End A5.3
# Uncomment for pasting
"""
try:
    path = sys.argv[1]
except IndexError as ie:
    print("Please give an argument.\nRunning with args[1] = \"test_file\"")
    path = "test_file"

dic = json.loads(input())
t = (dic["source"], dic["destination"], bytes.fromhex(dic["data"]))
packet = build_udp_packet(t[0], t[1], t[2])
bin_file = open(path, "wb")
bin_file.write(packet)
bin_file.close()
"""
# End A5.4