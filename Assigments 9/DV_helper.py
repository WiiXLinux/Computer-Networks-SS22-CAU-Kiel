# This statement specifies explicitly which functions are
# imported when another script calls "import DV_helper"
from __future__ import annotations

__all__ = (
    'send_to',
    'cost',
    'get_next_table',
    'print_routing_table'
)

from copy import deepcopy
from threading import Thread
from time import sleep
from math import inf, nan
from queue import Empty, Queue
from random import random
from sys import stderr

_rt_queue = Queue(0)

# This should be true after the first load of this module
_is_initialized = False

_nodes = {
    0: (0.0, [[nan, nan, nan, nan, nan, nan]]),
    1: (2.0, [
        [2.0, 0.0, 1.0, inf, 11.0, inf],
        [2.0, 0.0, 1.0, 4.0, 11.0, 12.0],
        [2.0, 0.0, 1.0, 4.0, 5.0, 12.0],
        [2.0, 0.0, 1.0, 4.0, 5.0, 7.0],
        [2.0, 0.0, 1.0, 4.0, 5.0, 7.0]
    ]),
    5: (10.0, [
        [10.0, inf, inf, inf, 2.0, 0.0],
        [10.0, 12.0, inf, 3.0, 2.0, 0.0],
        [10.0, 12.0, 6.0, 3.0, 2.0, 0.0],
        [10.0, 7.0, 6.0, 3.0, 2.0, 0.0],
        [9.0, 7.0, 6.0, 3.0, 2.0, 0.0]
    ]),
}
_node_count = 6


def _put_in_queue_after_delay(item, queue: Queue):
    t = random() / 4
    sleep(t)
    queue.put(item)


def send_to(node_id: int, update_table: list[float]):
    if not isinstance(node_id, int):
        raise TypeError(f'node_id must be int, was {type(node_id)}.')
    elif node_id not in _nodes:
        raise ValueError(f'{node_id} is not connected to your node.')
    else:
        # Here is the logic that controls what happens next

        # Print the table and the node it is directed at
        # print(f'Sending to {node_id}:', file=stderr)
        # print(*(f'To {node_id} with cost: {cost}' for node_id, cost in enumerate(update_table)), sep=', ', file=stderr)

        # Don't simulate an answer to yourself
        if node_id != 0:
            answers_list = _nodes[node_id][1]
            # Get the expected response
            response = answers_list.pop(0)
            # Queue the response in (but after a small delay, since we use threads here)
            t = Thread(target=_put_in_queue_after_delay, args=((node_id, response), _rt_queue))
            if not answers_list:
                # If we got the last response add (a copy of) it, otherwise drop it
                answers_list.append(deepcopy(response))
            t.start()


def cost(to_node: int) -> float:
    if not isinstance(to_node, int):
        raise TypeError(f'to_node must be int, was {type(to_node)}.')
    elif to_node >= _node_count:
        raise ValueError(f'{to_node} is not a node.')
    elif to_node in _nodes:
        return _nodes[to_node][0]
    else:
        return inf


def get_next_table(block=True, timeout=None) -> tuple[int, list[float]] | None:
    try:
        return _rt_queue.get(block, timeout)
    except Empty:
        return None


def print_routing_table(routing_table: list[tuple[float, int]]):
    entries = []
    # enumerate() produces tuples of indices and corresponding entries of the given list
    for index, entry in enumerate(routing_table):
        entries.append('({0:2}, {1[0]:3.3g}, {1[1]:2})'.format(index, entry))
    print(",".join(entries))
    """
    # We can also accomplish this with some Python magic
    print(*( # We use a generator comprehension which we unpack to generate an
             # argument for each entry in the routing table
        '({0:2}, {1[0]:3.3g}, {1[1]:2})'.format(*entry) # format this entry
        for entry in enumerate(routing_table)
    ), sep=',') # separate the args with a comma.
    """


def _init():
    # Set initialized flag
    global _is_initialized
    _is_initialized = True

    for node_id, config in _nodes.items():
        # Put the initial broadcast into the queue
        if node_id != 0:
            answer_list = config[1]
            # Get the expected response
            response = answer_list.pop(0)
            # Queue the response in (but after a small delay, we use threads here)
            t = Thread(target=_put_in_queue_after_delay, args=((node_id, response), _rt_queue))
            if not answer_list:
                # If we got the last response, add (a copy of) it, otherwise drop it
                answer_list.append(deepcopy(response))
            t.start()


if not _is_initialized:
    _init()
