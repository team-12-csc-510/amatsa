"""Client Code integrates all metrics and send to Elastic Server"""

import logging
import os
import sys
import time
from datetime import datetime

from dotenv import load_dotenv
from elasticsearch import Elasticsearch
from elasticsearch.exceptions import (
    BadRequestError,
    ConflictError,
    ConnectionError,
    NotFoundError,
    SerializationError,
    SSLError,
    TransportError,
)
from pyJoules.energy_meter import measure_energy  # type: ignore
from pyJoules.handler.pandas_handler import PandasHandler  # type: ignore

from src.disk import Disk
from src.file_monitoring import FileMonitoring
from src.gpu import GPUdata
from src.network import Network
from src.process import ProcessMeta
from src.system import System
from src.utils import get_config

pandas_handler = PandasHandler()

load_dotenv()  # take environment variables from .env.


def ReadFileMonitoringFile(filename):
    """This method parses data from the file and returns a dictionary object

    :param filename: name of file containing data to be extracted in the dictionary"""
    file_dict = {}
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", filename)
    if os.path.exists(path):
        with open(path, "r") as file:
            file_data = file.readlines()
            for data in file_data:
                print(data)
                data_ls = data.split(" ")
                if data_ls[1] not in file_dict:
                    file_dict[data_ls[1]] = []
                file_dict[data_ls[1]].append(data_ls[0])
        return file_dict
    else:
        return None


@measure_energy(handler=pandas_handler)
def CollectMetrics(obj: dict) -> bool:
    """This method collects client metrics and returns them in a json

    The measure_energy decorator is used to send a pandas data frame
    containing information regarding the energy consumption of the host
    machine"""
    # empty json objects
    agent: dict = {}
    metrics: dict = {}
    netw: dict = {}

    try:
        # instances for data collection
        fs = Disk()
        sy = System()
        net = Network()

        # read data from the file
        filename = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "..",
            FileMonitoring().get_filename(),
        )
        obj["file_data"] = ReadFileMonitoringFile(filename)

        # delete data from the file
        file = open(filename, "w")
        file.close()

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
        val = process_data.retrieve_process_info()
        obj["high_memory_process"] = val[1]
        obj["high_cpu_process"] = val[0]
    except Exception as e:
        logging.error(
            str(time.time()) + " " + str(e) + "occurred while collecting client metrics"
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
    status = True

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
    try:
        # push to elastic
        hosts_config = config["connect"]["endpoint"]
        # ssl_fingerprint = config["connect"]["tls-fingerprint"]
        es = Elasticsearch(
            hosts=[{"host": "localhost", "port": 9200, "scheme": "http"}],
            basic_auth=token,
            verify_certs=False,
        )
        resp = es.index(index=config["index"]["name"], document=client_json)
    except (
        ConnectionError,
        SSLError,
        TransportError,
        SerializationError,
        BadRequestError,
        ConflictError,
        NotFoundError,
    ) as e:
        logging.exception(
            str(time.time()) + " " + str(e) + "occured while using elastic search"
        )
        print("Failed to send data to backend", file=sys.stderr)
        sys.exit(1)
