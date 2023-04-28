import sys

input_file = sys.argv[1]
output_file = sys.argv[2]
keyphrase = sys.argv[3]
keyphrase = keyphrase.encode()

f1 = open(input_file, "rb")
f2 = open(output_file, "wb")

data = f1.read()
key_len = len(keyphrase)

for i in range(len(data)):
    key_byte = keyphrase[i % key_len]
    f2.write(bytes([data[i] ^ key_byte]))
