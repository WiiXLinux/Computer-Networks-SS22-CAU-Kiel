from socket import *
import sys


serverAddress = ""
serverPort = 0

try:
    serverAddress = sys.argv[1]
    serverPort = int(sys.argv[2])


except:
    try:
        if sys.argv[1] == "--help":
            print("usage: python client.py [--help] \nor python client.py (serverAddress) (serverPort)")
            exit(0)
    except:
        pass
    print("No valid input given, please specify serverAddress and serverPort")
    exit(-1)


clientSocket = socket(AF_INET, SOCK_DGRAM)

try:
    while True:
        try:
            clientSocket.sendto(input().encode(), (serverAddress, serverPort))
            data = clientSocket.recvfrom(2048)[0]
            print(data.decode().removesuffix("\n"))
        except EOFError:
            break
except KeyboardInterrupt:
    clientSocket.close()
    print("exiting...")


