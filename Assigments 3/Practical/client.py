from socket import *
import sys


try:
    serverAddress = sys.argv[1]
    serverPort = int(sys.argv[2])
except:
    print("No valid input given")
    serverAddress = "localhost"
    serverPort = 12345


clientSocket = socket(AF_INET, SOCK_DGRAM)

while True:
    try:
        clientSocket.sendto(input().encode(), (serverAddress, serverPort))
        data = clientSocket.recvfrom(2048)[0]
        print(data.decode().removesuffix("\n"))
    except:
        break


