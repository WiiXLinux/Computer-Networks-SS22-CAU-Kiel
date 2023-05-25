# A 1, 2, 3


from struct import pack


def parse_address(address: str) -> bytes:
    addresses = []
    for n in address.split('.'):
        addresses.append(int(n))

    return pack("!BBBB", addresses[0], addresses[1], addresses[2], addresses[3])  # BBBB!!!!!!?!?!?!!


# print(parse_address("192.168.1.1"))

# E 1

def prefix_matches(prefix: bytes, prefix_length: int, address: bytes) -> bool:  # MAGIC POWERS!
    def bin32(x):
        return ''.join(reversed([str((x >> i) & 1) for i in range(32)]))

    for i in range(prefix_length):
        if bin32(int.from_bytes(prefix, "big"))[i] != bin32(int.from_bytes(address, "big"))[i]:
            return False

    return True


# print(prefix_matches(parse_address("192.168.1.1"), 32, parse_address("192.168.1.10")))

# E 2

def route(routing_table: list, dest_ip: str):
    def takelen(elem):
        return elem["length"]

    routing_table.sort(key=takelen, reverse=True)

    for b in routing_table:
        if prefix_matches(b["prefix"], b["length"], parse_address(dest_ip)):
            return b["route"]

    return None


# E 3

"""
routing_table = [
    {'prefix': b'\x61\x62\x00\x00', 'length': 16, 'route': 'interface_a'},  # 97.98.0.0/16
    {'prefix': b'\x01\x01\x00\x00', 'length':  8, 'route': 'interface_b'},  # 1.1.0.0/8
    {'prefix': b'\x01\x01\x00\xF0', 'length': 29, 'route': 'interface_c'},  # 1.1.0.240/29
    {'prefix': b'\x00\x00\x00\x00', 'length':  0, 'route': 'default'},      # 0.0.0.0/0
    {'prefix': b'\x7f\x00\x00\x00', 'length':  8, 'route': 'lo'},           # 127.0.0.0/8
]

print(route(routing_table, "1.1.0.240"))
print(b'\x01\x01\x00\xF0'[0], b'\x01\x01\x00\xF0'[1], b'\x01\x01\x00\xF0'[2], b'\x01\x01\x00\xF0'[3])
"""
