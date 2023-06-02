import struct
import sys


def parse_ipv4_datagram(datagram: bytes) -> tuple[bytes, bytes, int, bytes]:
    ip_from = datagram[12:16]
    ip_to = datagram[16:20]
    protocol = datagram[9]
    data = datagram[20:len(datagram)]
    return ip_from, ip_to, protocol, data


# Testing:
"""
parse_ipv4_datagram(bytes.fromhex('''
45 00
00 3c 43 eb 00 00 ff 11  24 20 c0 a8 b2 01 e0 00
00 fb 14 e9 14 e9 00 28  32 84 8b 3e 01 00 00 01
00 00 00 00 00 00 08 75  62 75 6e 74 75 2d 38 05
6c 6f 63 61 6c 00 00 ff  00 01
'''))
"""


def inet_checksum(data: bytes) -> int:
    """
    Calculate the internet checksum for data. The internet checksum is the ones
    complement sum of the 16 bit segments in the data
    """
    # first calculate the twos complement sum
    twos_complement_sum: int = 0

    # let i be every second index into data
    for i in range(0, len(data), 2):
        word: int
        # convert 2 bytes from i as an unsigned 16 bit big-endian integer
        word, = struct.unpack('!H', data[i:i + 2])
        # then add `word` to the twos complement sum
        twos_complement_sum += word

    # Then, convert the twos complement sum into ones complement by folding
    # around the carry
    ones_comp_sum = twos_complement_sum

    while ones_comp_sum >> 16:
        ones_comp_sum = (ones_comp_sum >> 16) + (ones_comp_sum & 0xFFFF)

    return ~ones_comp_sum & 0xFFFF


def modify_ipv4_datagram(datagram: bytes, new_src_addr: bytes, new_dest_addr: bytes, new_body: bytes) -> bytes:
    temp = bytearray(datagram)
    temp[12:16] = new_src_addr
    temp[16:20] = new_dest_addr
    temp[20:len(datagram)] = new_body
    temp[10:12] = bytes.fromhex("0000")
    temp[10:12] = struct.pack("!H", inet_checksum(bytes(temp[:20])))
    return temp


# Testing:
'''
datagram = bytes.fromhex("""
45 00 00 3c 43 eb 00 00  ff 11 24 20 c0 a8 b2 01
e0 00 00 fb 14 e9 14 e9  00 28 32 84 8b 3e 01 00
00 01 00 00 00 00 00 00  08 75 62 75 6e 74 75 2d
38 05 6c 6f 63 61 6c 00  00 ff 00 01
""")

result = modify_ipv4_datagram(datagram, b'aaaa', b'\xff\xab\xcd\xef', bytes.fromhex("""
    ab cd ef 01 02 34 56 78  8b 3e 01 99 00 01 00 12
    00 00 00 34 08 75 62 75  6e 74 75 55 38 05 6c 6f
    63 61 6c 17 00 ff 00 19
"""))

for i, b in enumerate(result):
    if i % 16 == 0:
        print(f'{i:05x}   ', end='')
    if i % 8 == 0:
        print(' ', end='')
    print(f'{b:02x} ', end='')
    if i % 16 == 15:
        print()
'''
# Key = lanPort, Value = wanPort. Ip that goes in has a port that also has to be translated.
# Key = wanPort, Value = lanPort. Ip that goes out has a port that also has to be translated.
_CN_portDict = {}
# Key = wanPort, Value = lanIp
_CN_ipDict = {}
_CN_maxPort = 1


def translate_addresses(datagram: bytes, interface: str, wan_addr: bytes) -> bytes:
    global _CN_portDict  # We need this to translate the ports
    global _CN_ipDict
    global _CN_maxPort
    # Copy to 10th byte (last byte of protocol), then add a zero checksum.
    newDatagram = datagram[:10] + bytes.fromhex("0000")  # Now at length 12. 8 bytes to go.
    ip_from, ip_to, protocol, data = parse_ipv4_datagram(datagram)
    if interface == "lan":  # So connection is outgoing from local network
        newDatagram += wan_addr  # Doesn't change, there is only one address, which is the "router" address.
        newDatagram += ip_to
        # Now at length 20

        sourcePort = data[0:2]  # Source port mentioned in payload, has to be translated

        try:
            # print(type(sourcePort), file=sys.stderr)
            newDatagram = newDatagram + _CN_portDict[sourcePort]  # Add translated source port
        except KeyError:  # If the source port is not registered yet,
            _CN_portDict[struct.pack("!h", _CN_maxPort)] = sourcePort  # give it a
            _CN_portDict[sourcePort] = struct.pack("!h", _CN_maxPort)  # translation port
            _CN_ipDict[struct.pack("!h", _CN_maxPort)] = ip_from  # Add an entry to the port to lan Ip database
            _CN_maxPort += 1

            newDatagram += _CN_portDict[sourcePort]  # Then add translated source port

        destinationPort = data[2:4]  # Add destination port mentioned in payload, stays the same
        newDatagram += destinationPort

        # Now at length 20 + 4

    elif interface == "wan":  # So connection is incoming to local network
        newDatagram += ip_from
        newDatagram += _CN_ipDict[data[2:4]]  # Add the translated destination ip address
        # Now at length 20

        sourcePort = data[0:2]  # Source port mentioned in payload
        newDatagram += sourcePort

        destinationPort = data[2:4]  # Destination port mentioned in payload. Has to be translated

        try:
            newDatagram += _CN_portDict[destinationPort]  # Add translated destination port
        except KeyError:
            print("There was no value for the destination port: " + str(int.from_bytes(destinationPort, "big")))

        # Now at length 20 + 4
    else:
        raise Exception("Wrong interface: \"" + interface + "\"")

    newDatagram += data[4:]  # Add the rest that remains unchanged

    return newDatagram


'''
datagram = bytes.fromhex("""
45 00 00 3c 43 eb 00 00  ff 11 24 20 c0 a8 b2 01
e0 00 00 fb 14 e9 14 e9  00 28 32 84 8b 3e 01 00
00 01 00 00 00 00 00 00  08 75 62 75 6e 74 75 2d
38 05 6c 6f 63 61 6c 00  00 ff 00 01
""")

print("_CN_maxPort: " + str(_CN_maxPort), "_CN_portDict: " + str(_CN_portDict), "_CN_ipDict: " + str(_CN_ipDict))

result = translate_addresses(datagram, "lan", bytes.fromhex("11 11 11 11"))

print("_CN_maxPort: " + str(_CN_maxPort), "_CN_portDict: " + str(_CN_portDict), "_CN_ipDict: " + str(_CN_ipDict))

for i, b in enumerate(result):
    if i % 16 == 0:
        print(f'{i:05x}   ', end='')
    if i % 8 == 0:
        print(' ', end='')
    print(f'{b:02x} ', end='')
    if i % 16 == 15:
        print()
'''
