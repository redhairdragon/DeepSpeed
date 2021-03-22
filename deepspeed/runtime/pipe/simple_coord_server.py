import torch.distributed as dist
from datetime import timedelta

TCP_STORE_PORT = 8877
NUM_WORKERS = 2  # TODO make it configurable
server_store = dist.TCPStore(
    "0.0.0.0", TCP_STORE_PORT, NUM_WORKERS, True, timedelta(seconds=30)
)


def set_remapping():
    server_store.set("remapping", "1")


while True:
    usr_in = input()
    set_remapping()
