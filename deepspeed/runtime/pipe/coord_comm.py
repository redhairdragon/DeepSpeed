import torch
import torch.distributed as dist
import boto3
from datetime import timedelta

# communication class for pipe engine
# use to determine:
#   1. remapping is happening or not
#   2. store remapping related variable TODO: move this to each worker
TCP_STORE_PORT = 8877


class CoordComm:
    def __init__(self, coord_server_name="coord"):
        self.private_ip = self.get_coord_server_ip(coord_server_name)
        self.port = TCP_STORE_PORT
        self.client_store = dist.TCPStore(
            self.private_ip, TCP_STORE_PORT, False, timedelta(seconds=30))

    def check_reconfiguration(self):
        return self.client_store.get('remapping')

    # get the name of coord server
    def get_coord_server_ip(self, coord_server_name):
        client = boto3.client('ec2')
        response = client.describe_instances(
            Filters=[{
                "Name": "tag:Name",
                "Values": [coord_server_name]
            }]
        )
        private_ips = []
        for insts in response['Reservations']:
            for inst in insts["Instances"]:
                if "PrivateIpAddress" in inst and inst['State']['Name'] == 'running':
                    private_ips = inst["PrivateIpAddress"]

        assert len(private_ips) == 1,\
            f"No Instance named {coord_server_name}\n/Multiple Instances named {coord_server_name} as coordinates server"
        return private_ips[0]

    def setStateDict(self, name, state):
        self.client_store.set(name, state)

    def getStateDict(self, name):
        self.client_store.wait(name)
        state_dict_raw = self.client_store.get(name)
        self.client_store.delete(name)
        return torch.load(state_dict_raw)
