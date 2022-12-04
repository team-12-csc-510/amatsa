"""Client Code integrates all metrics and send to Elastic Server"""

import logging
import sys
import time
from datetime import datetime

import elasticsearch as k
from dotenv import load_dotenv
from elasticsearch import Elasticsearch
from pyJoules.energy_meter import measure_energy
from pyJoules.handler.pandas_handler import PandasHandler

from src.disk import Disk
from src.gpu import GPUdata
from src.network import Network
from src.process import ProcessMeta
from src.system import System
from src.utils import get_config

pandas_handler = PandasHandler()


load_dotenv()  # take environment variables from .env.


@measure_energy(handler=pandas_handler)
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
        obj["high_memory_processes"] = process_data.top_memory
        obj["high_cpu_processes"] = process_data.top_cpu
        # converting to json string
    except Exception as e:
        logging.error(time, e, "occurred while collecting client metrix")
        return False

    return True


if __name__ == "__main__":
    client_json = {}
    error_list = [k.ApiError, k.AuthenticationException, k.AuthorizationException]
    error_list.extend(
        [
            k.BadRequestError,
            k.ConflictError,
            k.ConnectionError,
            k.ConnectionTimeout,
            k.NotFoundError,
        ]
    )
    error_list.extend(
        [k.SerializationError, k.SSLError, k.TransportError, k.UnsupportedProductError]
    )
    error_list1 = tuple(error_list)
    # read config from yml file
    config = get_config()
    # collect meta-data fields
    version = config["version"]
    client_json["metadata"] = {
        "version": version,
        "time": datetime.utcnow().isoformat() + "Z",
    }
    token = (config["auth"]["username"], config["auth"]["password"])

    try:
        status = CollectMetrics(client_json)
    except Exception as e:
        logging.error(e, exc_info=True)

    if not status:
        sys.exit(1)
    # client_json = json.dumps(client_json, indent=2)
    # call pickle function with network creds.
    print("final_json", client_json)
    df2 = {}
    try:
        df = pandas_handler.get_dataframe()
        df2 = df.to_json(orient="columns")

    except Exception as e:
        logging.error(e)

    client_json["energy"] = df2
    # client_json = client_json + df2
    try:
        # push to elastic
        hosts_config = config["connect"]["endpoint"]
        # ssl_fingerprint = config["connect"]["tls-fingerprint"]
        es = Elasticsearch(hosts=hosts_config, verify_certs=False, basic_auth=token)
        resp = es.index(index=config["index"]["name"], document=client_json)
    except error_list1 as e:
        logging.exception(
            str(time.time()) + " " + str(e) + "occured while using elastic search"
        )
        print("Failed to send data to backend", file=sys.stderr)
        sys.exit(1)
