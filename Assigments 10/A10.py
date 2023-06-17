# Task 1

def convert_and_pad(data: bytes, padding_length: int) -> int:
    """
    Converts data into int with padding_length 0 bits.

    >> print(hex(convert_and_pad(bytes.fromhex("abcdef"), 4)))
    0xabcdef0
    >> print(hex(convert_and_pad(bytes.fromhex("abcdef"), 16)))
    0xabcdef0000
    >> print(hex(convert_and_pad(b"foo", 15)))
    0x3337b78000

    :param data: data to be converted
    :param padding_length: number of added 0 bits
    :return: int of (data + 0 * padding_length)
    """

    value = int.from_bytes(data, 'big')
    newValue = (value << padding_length)

    return newValue


def is_bit_set(i: int, n: int) -> bool:
    """
    Returns if the nth bit of i is set or not

    >> is_bit_set(0, 0)
    False
    >> is_bit_set(1, 0)
    Tue
    >> is_bit_set(2, 1)
    True

    :param i: Number to be checked.
    :param n: Bit indicator of i
    :return: is nth bit of i set?
    """

    mask = 1 << n
    return i & mask == mask


def IO_array_XOR(io_1, io_2):
    temp = []
    for i in range(len(io_1)):
        temp.append(io_1[i] ^ io_2[i])
    return temp


def int_to_IO_array(i: int) -> list[int]:
    temp = []
    for n in bin(i)[2:]:
        temp.append(int(n))
    return temp


def crc(data: bytes, generator: int, generator_length: int) -> int:
    """
    Implementation of crc
    :param data: Data to be hashed (D)
    :param generator: Generator (G)
    :param generator_length: Length of the generator (r)
    :return: crc of D
    """
    # pad the input
    padded_input = convert_and_pad(data, generator_length - 1)  # r - 1

    # convert to 1/0 list
    i_arr_padded_input = int_to_IO_array(padded_input)
    print(i_arr_padded_input)

    # get first mask
    mask = int_to_IO_array(generator)[:generator_length]  # sonst ist das zu groß komischerweise.
    # and first slice
    slice1 = i_arr_padded_input[:generator_length]
    print(len(slice1))
    print(len(mask))


    i = 0
    somebits = []
    while True:
        res = IO_array_XOR(slice1, mask)
        print("   " * (i) + str(slice1))
        print("   " * (i) + str(mask))
        try:
            slice1 = res[1:] + [i_arr_padded_input[i + generator_length]]
        except IndexError:
            somebits = slice1
            break


        if slice1[0] == 1:
            mask = int_to_IO_array(generator)[:generator_length]
        else:
            mask = [0] * generator_length
        i += 1

    i_arr_padded_input = i_arr_padded_input[:len(i_arr_padded_input) - (generator_length - 1)] + somebits
    print(i_arr_padded_input)
    toS = ""
    for bit in somebits:
        toS += str(bit)
    return int(toS, 2)


result = crc(int('1101011111', 2).to_bytes((int('1101011111', 2).bit_length() + 7) // 8, "big"), int('10011', 2), 5)
# print the result nicely in hexadecimal
print(f'The crc is {result:#06x}')

data = b'foobarbaz!'
# this is the generator polynom used by binascii.crc_hqx(...)
generator = 0x11021

result = crc(data, generator, 16)

# print the result nicely in hexadecimal
print(f'The crc is {result:#06x}')
