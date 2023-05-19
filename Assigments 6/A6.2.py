import copy
import struct
import sys
from zlib import crc32
from udt_socket import udt_send, udt_recv, start_sender


def is_corrupt(data_message: bytes) -> bool:
    checksum = int.from_bytes(data_message[0:4], "big")
    seq_and_data = data_message[4:24]
    realChecksum = crc32(seq_and_data)
    return realChecksum != checksum


def extract_data(data_message: bytes) -> tuple[int, bytes]:
    return int.from_bytes(data_message[4:8], "big"), data_message[8:24]


NAK = b'\xbe\xbc\xb4\xde'
ACK = b'ACK!'
realMessage = None

"""
Sadly only works for messages that are not bigger than the container in one packet. :(

def rdt_recv() -> bytes:
    global realMessage
    data = udt_recv()
    print("[RECEIVER] received message:", data.hex(" "))
    if is_corrupt(data):
        udt_send(struct.pack("!I4s", crc32(NAK), NAK))
        print("[RECEIVER] data corrupt, sending NAK")
        return rdt_recv()
    else:
        if data == bytes.fromhex("88 73 50 ce 00 00 00 01 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00"):
            print("[RECEIVER] got EOT, exiting")
            clone = copy.copy(realMessage)
            realMessage = None
            return clone

        print("[RECEIVER] data fine, sending ACK")
        if realMessage is None:
            realMessage = data

        udt_send(struct.pack("!I4s", crc32(ACK), ACK))
        return rdt_recv()
"""


def rdt_recv():
    temp = b""
    data = udt_recv()

    while data != b'\x88sP\xce\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'\
            and data != b'\x88sP\xce\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00':
        temp += data[8:24]
        udt_send(struct.pack("!I4s", crc32(ACK), ACK))
        data = udt_recv()
    print("Received EOF, dying")
    udt_send(struct.pack("!I4s", crc32(ACK), ACK))

    # slice the 0's off temp
    notYet = True
    slicer = len(temp)
    for i in range(len(temp)):
        if notYet:
            if temp[len(temp) - i - 1] == 0:
                slicer -= 1
            else:
                notYet = False
        else:
            break

    return temp[:slicer]


start_sender(b'testing is a bitch, I just want to die')
print(rdt_recv().decode(), file=sys.stderr)

exit(1)
