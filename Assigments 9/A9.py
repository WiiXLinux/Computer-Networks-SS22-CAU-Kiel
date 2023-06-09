import copy
import math
from DV_helper import send_to, cost, get_next_table, print_routing_table


def print_environment():
    costs = []
    counter = 0
    while True:
        try:
            costs.append(cost(counter))
        except:
            break
        counter += 1

    for i, c in enumerate(costs):
        if c != math.inf:
            print(f"Connection to {i} with cost {c}")
    print(f"There are {counter} nodes in total")


# Test
# print_environment()

# It works :)
# Don't forget to include the imports...
def update(old_table: list[tuple[float, int]], received_vector: list[float], received_from: int) -> list[tuple[float, int]]:
    # For each destination
    for i in range(1, len(received_vector)):
        # If a route that was used has an updated cost, update the cost
        if old_table[i][1] == received_from:
            old_table[i] = (received_vector[i] + cost(received_from), received_from)

        # Calculate minimum
        nextT = (min(old_table[i][0], cost(received_from) + received_vector[i]), -1)

        # "Calculate" next route point
        # If the cost stays the same, reuse the old route.
        if nextT[0] == old_table[i][0]:
            nextT = (nextT[0], old_table[i][1])
        # If the new route is faster, change the next route point
        else:
            nextT = (nextT[0], received_from)
        # Update old_table by mutating it
        old_table[i] = nextT
    # Return the new routing table
    return old_table


def distance_vector_algorithm(max_times=-1):
    # START OF INITIALISATION
    costs = []
    index = 0
    # init costs
    while True:
        try:
            costs.append(cost(index))
            index += 1
        except ValueError:
            index = 0
            break

    #print(costs)

    n = len(costs)
    routing_table = [(0.0, 0)] * n

    # init routing table
    for i, c in enumerate(costs):
        if c != math.inf:
            routing_table[i] = (c, i)
        else:
            routing_table[i] = (math.inf, -1)

    print_routing_table(routing_table)

    # tell neighbours your costs
    for i in range(n):
        try:
            send_to(i, costs)
        except ValueError:
            pass

    # END OF INITIALISATION
    # START OF LOOP
    # if timeout == 3, break and end the program
    timeout = 0
    counter = 0
    old_routing_table = None
    while timeout != 3 and counter != max_times:
        counter += 1
        # get the next distance vector from a neighbour
        next_distance_vector = get_next_table()

        # if there is none, timeout++ and repeat
        if routing_table == old_routing_table or next_distance_vector is None:
            timeout += 1
            continue

        old_routing_table = copy.copy(routing_table)

        # reset timeout so that after getting a distance vector you don't start crying
        # because you remember you didn't get one last time
        timeout = 0
        # update the internal routing table
        routing_table = update(routing_table, next_distance_vector[1], next_distance_vector[0])

        print_routing_table(routing_table)

        # update the costs
        costs = []
        while True:
            try:
                costs.append(cost(index))
                index += 1
            except ValueError:
                index = 0
                break

        # notify the others
        for i in range(n):
            try:
                send_to(i, costs)
            except ValueError:
                pass


distance_vector_algorithm()



"""
Expected output from test 1
( 0,   0,  0),( 1,   2,  1),( 2, inf, -1),( 3, inf, -1),( 4, inf, -1),( 5,  10,  5)
( 0,   0,  0),( 1,   2,  1),( 2,   3,  1),( 3, inf, -1),( 4,  12,  5),( 5,  10,  5)
( 0,   0,  0),( 1,   2,  1),( 2,   3,  1),( 3,   6,  1),( 4,  12,  5),( 5,  10,  5)
( 0,   0,  0),( 1,   2,  1),( 2,   3,  1),( 3,   6,  1),( 4,   7,  1),( 5,  10,  5)
( 0,   0,  0),( 1,   2,  1),( 2,   3,  1),( 3,   6,  1),( 4,   7,  1),( 5,   9,  1)

Output from test 1
( 0,   0,  0),( 1,   2,  1),( 2, inf, -1),( 3, inf, -1),( 4, inf, -1),( 5,  10,  5)
( 0,   0,  0),( 1,   2,  1),( 2,   3,  1),( 3, inf, -1),( 4,  13,  1),( 5,  10,  5)
( 0,   0,  0),( 1,   2,  1),( 2,   3,  1),( 3, inf, -1),( 4,  12,  5),( 5,  10,  5)
( 0,   0,  0),( 1,   2,  1),( 2,   3,  1),( 3,   6,  1),( 4,  12,  5),( 5,  10,  5)
( 0,   0,  0),( 1,   2,  1),( 2,   3,  1),( 3,   6,  1),( 4,  12,  5),( 5,  10,  5)
"""
