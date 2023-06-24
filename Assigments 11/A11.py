# FIRST TASK

import json
import socket
from sys import argv, exit


def main() -> int:
    # read in the port argument
    udp_port = int(argv[1]) if len(argv) > 1 else 9009

    # if the wrong number of arguments are provided, print a usage message
    if len(argv) != 2:
        print(f'Usage: python {argv[0]} [port]')

    # TODO: listen for incoming requests on `udp_port`
    # Create UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # sock.setblocking(False)
    sock.bind(("127.0.0.1", udp_port))

    while True:
        data, addr = sock.recvfrom(4096)

        # print(f"RECEIVED FRAME FROM: {addr}")
        # print(f"DATA: {data.decode()}")

        # TODO: decode the received request

        DICT = json.loads(data.decode())
        # print(DICT)
        print(f'Forwarding request: Frame from {DICT["source_mac"]} to {DICT["dest_mac"]} at interface {DICT["interface"]} with id {DICT["id"]}')

        # TODO: send the response requested by the task.

        response_DICT = {"id": DICT["id"], "forward_to": -1}

        # For this task, flood
        sock.sendto(json.dumps(response_DICT).encode("utf-8"), addr)

    # Program successfully terminated
    return 1


if __name__ == '__main__':
    # this will only be run when starting this file from the console, and not
    # when this file is imported. This can help you with testing individual
    # functions as you can call them individually from an interactive python
    # interpreter without starting your program
    exit(main())


# SECOND TASK
def decide_forwarding(forwarding_table: dict, forwarding_request: dict) -> tuple[dict, dict]:
    # forwarding_table stores key-value pairs in the format: {DESTINATION_MAC: FORWARD_TO}

    # for any incoming transmission, check if the incoming address is new.
    # If it is, add an entry to the forwarding_table with the incoming link as the forward_to.
    incoming_link = forwarding_request["interface"]
    incoming_addr = forwarding_request["source_mac"]
    forwarding_table[incoming_addr] = incoming_link

    # get destination mac and id of frame
    outgoing_addr = forwarding_request["dest_mac"]
    id = forwarding_request["id"]

    # if the forwarding_table's entry to any destination mac is empty, flood with forward_to -1
    outgoing_link = -1
    try:
        outgoing_link = forwarding_table[outgoing_addr]
    except KeyError:
        pass

    # return the mutated forwarding table and build request
    return forwarding_table, {"id": id, "forward_to": outgoing_link}
