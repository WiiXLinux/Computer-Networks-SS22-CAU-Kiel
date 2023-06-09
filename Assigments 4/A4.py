# START A4.1
# START A4.2
from urllib.parse import urlparse


def build_get_request(url: str) -> bytes:
    netloc, path = urlparse(url)[1:3]
    temp = "GET " + path + " HTTP/1.1\r\nConnection: close\r\nHost: " + netloc + "\r\n\r\n"
    return bytes(temp.encode())


# END A4.1

from socket import *
import sys


def TCP_client(url: str) -> None:
    serverPort = urlparse(url).port
    serverAddress = str(urlparse(url)[1]).removesuffix(":" + str(serverPort))
    if serverPort is None:
        serverPort = 80

    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((serverAddress, serverPort))

    while True:
        try:
            clientSocket.sendall(build_get_request(url))
            data = clientSocket.recvfrom(2048)[0]
            if data == b'':
                break
            print(data.decode(), end='')
        except EOFError:
            break
    clientSocket.close()


TCP_client(sys.argv[1])

# END A4.2
