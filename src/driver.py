"""Client Code integrates all metrics and send to Elastic Server"""

import os
import sys
import time
from datetime import datetime
import logging

import yaml
import elasticsearch as k
from elasticsearch import Elasticsearch

from src.disk import Disk
from src.gpu import GPUdata
from src.network import Network
from src.system import System


def CollectMetrics(obj: dict) -> bool:
    """This method collects client metrics and returns them in a json"""
    # empty json objects
    agent: dict = {}
    metrics: dict = {}
    netw: dict = {}

    try:
        # instances for data collection
        fs = Disk()
        sy = System()
        net = Network()
        # disk info
        client_disk_info = fs.retrieve_disk_info()
        obj["disk"] = client_disk_info
        # system info
        sy.FillSystemInfo(json=agent)
        sy.FillSystemMetrics(json=metrics)
        obj["agent"] = agent
        obj["metrics"] = metrics
        # network info
        net.get_network_info()
        net.fill_network_info(netw)
        obj["network"] = netw
        # gpu info
        client_gpu = GPUdata()
        gpu_info = client_gpu.retrieve_gpu_info()
        if not gpu_info:
            gpu_info = None
        obj["gpu"] = gpu_info
        # converting to json string
    except Exception as e:
        logging.error(time, e, "occurred while collecting client metrix")
        return False

    return True


if __name__ == "__main__":
    client_json = {}
    error_list = [k.ApiError, k.AuthenticationException, k.AuthorizationException]
    error_list.extend([k.BadRequestError, k.ConflictError, k.ConnectionError, k.ConnectionTimeout, k.NotFoundError])
    error_list.extend([k.SerializationError, k.SSLError, k.TransportError, k.UnsupportedProductError])
    error_list1 = tuple(error_list)
    # read config from yml file
    with open(
        os.path.dirname(os.path.realpath(__file__)) + "/config/amatsa-client.yml",
        "r",
        encoding="utf-8",
    ) as file:
        config = yaml.safe_load(file)
    # collect meta-data fields
    version = config["version"]
    client_json["metadata"] = {
        "version": version,
        "time": datetime.utcnow().isoformat() + "Z",
    }
    token = (config["auth"]["username"], config["auth"]["password"])
    if not CollectMetrics(client_json):
        sys.exit(1)
    # client_json = json.dumps(client_json, indent=2)
    print("final_json", client_json)
    try:
        # push to elastic
        hosts_config = config["connect"]["endpoint"]
        # ssl_fingerprint = config["connect"]["tls-fingerprint"]
        es = Elasticsearch(hosts=hosts_config, verify_certs=False, basic_auth=token)
        resp = es.index(index=config["index"]["name"], document=client_json)
    except error_list1 as e:
        logging.exception(time + str(e) + "occured while using elastic search")
        print("Failed to send data to backend", file=sys.stderr)
        sys.exit(1)
