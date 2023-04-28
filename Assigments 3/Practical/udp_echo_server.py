from socket import *
import sys


try:
    serverPort = int(sys.argv[1])
except:
    print("No valid port input given, setting port to 12345")
    serverPort = 12345


print("Starting UPD server on port:", serverPort)
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(("127.0.0.1", serverPort))
print("Server ready...")

while True:
    data, clientAddress = serverSocket.recvfrom(2048)
    print("message: \"", data.decode().removesuffix("\n"), "\" from:", clientAddress)
    serverSocket.sendto(data, clientAddress)


