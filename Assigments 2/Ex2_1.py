import sys

input_file = sys.argv[1]
output_file = sys.argv[2]

f1 = open(input_file, "rb")
f2 = open(output_file, "wb")

data = f1.read()
f2.write(data)
