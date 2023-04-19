import sys
if len(sys.argv) != 4:
    print("Usage: encrypt_file.py <input filename> <output filename> <keyphrase>")
    sys.exit(1)
    
input_file = sys.argv[1]
output_file = sys.argv[2]
keyphrase = sys.argv[3]
keyphrase = keyphrase.encode()

try:
    try:
        f1 = open(input_file, "rb")
    except FileNotFoundError:
        print("Error: Inputfile not found")
        sys.exit(1)
    try:
        f2 = open(output_file, "wb")
    except FileNotFoundError:
        print("Error: Outputfile not found")
        sys.exit(1)
    data = f1.read()
    key_len = len(keyphrase)

    for i in range(len(data)):
        key_byte = keyphrase[i%key_len]
        f2.write(bytes([data[i] ^ key_byte]))
except: 
    print("Error: Could be a lot of errors... For example the outputfile is not writeable")
