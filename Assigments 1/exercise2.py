import math

width = int(input())
i = input()
strings = []

while i != "END":
    strings.append(i)
    i = input()

lines = [None] * len(strings)

for index in range(len(strings)):
    left_index = math.ceil((width - len(strings[index])) / 2)
    right_index = math.floor((width - len(strings[index])) / 2)
    lines[index] = ["·" * left_index + strings[index] + "·" * right_index]
    print(lines[index][0])
