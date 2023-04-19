import json

# loads json into dict
dic = json.loads(input())

while True:
    i = input()
    try:
        print(dic[i])
    except KeyError:
        break
