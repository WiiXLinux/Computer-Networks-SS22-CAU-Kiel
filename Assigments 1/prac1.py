name = input()

while len(name) != 0:
    if name[0] == " ":
        name = name[1:]
    elif name[len(name) - 1] == " ":
        name = name[:len(name) - 1]
    else:
        break

if name == "":
    name = "stranger"

print("Hello " + name + "!")
