import sys
import os
import torch.distributed as dist
from datetime import timedelta

TCP_STORE_PORT = 8877

if __name__ == '__main__':
    server_store = dist.TCPStore(
        "0.0.0.0", TCP_STORE_PORT, 100, True, timedelta(seconds=30))
    server_store.set('remapping', '0')
    while True:
        pass
