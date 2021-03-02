import torch.distributed as dist
import boto3
import requests

# communication class for pipe engine


class CoordComm:
    def __init__(self, coord_server_name="coord", port="3000"):
        self.private_ip = self.get_coord_server_ip(coord_server_name)
        self.endpoint = self.private_ip + port
        self.session = requests.Session()

    def check_reconfiguration(self):
        resp = self.session.get(f'{self.endpoint}/status')
        return resp.text == 'YES'

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
            f"Multiple Instances named {coord_server_name} as coordinates server"
        return private_ips[0]
