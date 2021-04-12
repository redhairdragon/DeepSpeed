import torch.distributed as dist
from datetime import timedelta
from .constant import *

TCP_STORE_PORT = 8877
NUM_WORKERS = 2  # TODO make it configurable
server_store = dist.TCPStore(
    "0.0.0.0", TCP_STORE_PORT, NUM_WORKERS, True, timedelta(seconds=30)
)
server_store.set(REMAPPING_KEY, REMAPPING_NOT_HAPPENING)

def set_remapping():
    server_store.set(REMAPPING_KEY, REMAPPING_HAPPENING)

while True:

    if server_store.get(REMAPPING_KEY) == b"0":
        usr_in = input()
        set_remapping()
    else:
        server_store.wait([REMAPPING_COUNT])
        if server_store.get(REMAPPING_COUNT) == NUM_WORKERS:
            server_store.set(REMAPPING_KEY, REMAPPING_NOT_HAPPENING)
            server_store.delete_key(REMAPPING_COUNT)
