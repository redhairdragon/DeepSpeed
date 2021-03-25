import torch.distributed as dist
from datetime import timedelta

TCP_STORE_PORT = 8877
NUM_WORKERS = 2  # TODO make it configurable
server_store = dist.TCPStore(
    "0.0.0.0", TCP_STORE_PORT, NUM_WORKERS, True, timedelta(seconds=30)
)
server_store.set("remapping", "0")


def set_remapping():
    server_store.set("remapping", "1")


while True:
    if server_store.get("remapping") == b"0":
        usr_in = input()
        set_remapping()
    else:
        server_store.wait(["remapping_done_count"])
        if server_store.get("remapping_done_count") == NUM_WORKERS:
            server_store.set("remapping", "0")
            server_store.delete_key("remapping_done_count")
