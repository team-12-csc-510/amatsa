import os

import boto3


class AWS:
    def __init__(self, service_name: str):
        self.service_name = service_name


class AWSResource(AWS):
    def __init__(self, service_name: str):
        super().__init__(service_name)
        self._resource = boto3.resource(
            service_name,
            aws_access_key_id=os.environ["ACCESS_KEY"],
            aws_secret_access_key=os.environ["SECRET_KEY"],
        )

    @property
    def resource(self):
        return self._resource


class AWSClient(AWS):
    def __init__(self, service_name: str):
        super().__init__(service_name)
        self._client = boto3.client(
            service_name,
            aws_access_key_id=os.environ["ACCESS_KEY"],
            aws_secret_access_key=os.environ["SECRET_KEY"],
            region_name=os.environ["REGION_NAME"],
        )

    @property
    def client(self):
        return self._client
