"""Client Code integrates all metrics and send to Elastic Server"""

import logging
import sys
import time
from datetime import datetime

from dotenv import load_dotenv
from elasticsearch import Elasticsearch
from elasticsearch.exceptions import (
    ApiError,
    BadRequestError,
    ConflictError,
    ConnectionError,
    NotFoundError,
    RequestError,
    SerializationError,
    SSLError,
    TransportError,
    UnsupportedProductError,
)

from src.disk import Disk
from src.gpu import GPUdata
from src.network import Network
from src.process import ProcessMeta
from src.system import System
from src.utils import dump_list_to_json, get_config

load_dotenv()  # take environment variables from .env.


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
        process_data = ProcessMeta()
        obj["high_memory_processes"] = dump_list_to_json(process_data.top_memory)
        obj["high_cpu_processes"] = dump_list_to_json(process_data.top_cpu)
        # converting to json string
    except Exception as e:
        logging.error(
            str(time.time())
            .join(" ")
            .join(str(e))
            .join(" occurred while collecting client metrics")
        )
        return False

    return True


if __name__ == "__main__":
    client_json = {}
    # read config from yml file
    config = get_config()
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
    # call pickle function with network creds.
    print("final_json", client_json)
    try:
        # push to elastic
        hosts_config = config["connect"]["endpoint"]
        # ssl_fingerprint = config["connect"]["tls-fingerprint"]
        es = Elasticsearch(
            hosts=[{"host": "localhost", "port": 9200, "scheme": "http"}],
            verify_certs=False,
            basic_auth=token,
        )
        resp = es.index(index=config["index"]["name"], document=client_json)
    except (
        ApiError,
        ConnectionError,
        SSLError,
        TransportError,
        UnsupportedProductError,
        SerializationError,
        RequestError,
        BadRequestError,
        ConflictError,
        NotFoundError,
    ) as e:
        logging.exception(
            str(time.time()) + " " + str(e) + "occured while using elastic search"
        )
        print("Failed to send data to backend", file=sys.stderr)
        sys.exit(1)
