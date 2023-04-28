from socket import socket, AF_INET, SOCK_DGRAM
from sys import argv

def encrypt(message, key):
    key = key.encode("utf-8")
    message = message.encode('utf-8')
    encrypted = b''
    for i in range(len(message)):
        byte = message[i] ^ key[i % len(key)]
        encrypted += bytes([byte])
    return encrypted

def decrypt(message, key):
    key = key.encode('utf-8')
    decrypted = b''
    for i in range(len(message)):
        byte = message[i] ^ key[i % len(key)]
        decrypted += bytes([byte])
    return decrypted.decode('utf-8')


if len(argv) != 4:
    print('Usage: ' + argv[0] + ' <server_hostname> <port> <keyphrase>')
    exit(1)

server_host = argv[1]
server_port = int(argv[2])
server_address = (server_host, server_port)

keyphrase = argv[3]

name = input("")
encrypted_name = encrypt(name, keyphrase)

with socket(AF_INET, SOCK_DGRAM) as clientSocket:
    clientSocket.sendto(encrypted_name, server_address)
    
    encrypted_greeting, server_address = clientSocket.recvfrom(1024)
    greeting = decrypt(encrypted_greeting, keyphrase)

    print(greeting)