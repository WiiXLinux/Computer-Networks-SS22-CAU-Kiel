from zlib import crc32


def is_corrupt(data_message: bytes) -> bool:
    checksum = int.from_bytes(data_message[0:4], "big")
    seq_and_data = data_message[4:24]
    realChecksum = crc32(seq_and_data)
    return realChecksum != checksum


def extract_data(data_message: bytes) -> tuple[int, bytes]:
    return int.from_bytes(data_message[4:8], "big"), data_message[8:24]
