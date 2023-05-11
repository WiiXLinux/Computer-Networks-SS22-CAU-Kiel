example = bytes.fromhex(
    "00 35 ec f2 00 43 27 40  c6 0a 81 80 00 01 00 01"
    "00 00 00 00 02 64 73 0a  69 6e 66 6f 72 6d 61 74"
    "69 6b 08 75 6e 69 2d 6b  69 65 6c 02 64 65 00 00"
    "01 00 01 c0 0c 00 01 00  01 00 01 51 80 00 04 86"
    "f5 0a 67"
)

# Start A5.1

def parse_udp_packet(packet: bytes) -> (int, int, int, int, bytes):
    end = len(packet)
    return int.from_bytes(packet[0:2], "big"), int.from_bytes(packet[2:4], "big"), \
        int.from_bytes(packet[4:6], "big"), int.from_bytes(packet[6:8], "big"), packet[8:end]

# End A5.1

