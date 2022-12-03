#!/usr/bin/python
"""
This module fetches network information and returns a JSON with the network info data
"""
# pylint: disable=consider-using-f-string
import datetime
import logging
import socket
import time
import urllib.error
import urllib.request
from urllib.request import urlopen
from uuid import getnode as get_mac

import psutil
import speedtest  # type: ignore
import os
import pickle

from src.utils import check_time_delta, get_config

UNKNOWN = "unknown"


class Network:
    """Class to fetch, format and return network information"""

    mac_address = None
    ip_address = None
    hostname = None
    time_now = None
    down_speed = None
    up_speed = None
    speed_test = None
    connection_status = None
    addresses = None
    stats = None
    connected_interface = None

    def __init__(self):
        self.connection_status = False

    def connect_status(self):
        try:
            host = "http://google.com"
            with urlopen(host):  # Python 3.x
                self.connection_status = True
        except (urllib.error.HTTPError, urllib.error.URLError, urllib.error.ContentTooShortError) as e:
            logging.error(time, str(e), "occurred while opening http://google.com.")
            self.connection_status = False

    def get_network_info(self):
        self.connect_status()
        mac = get_mac()
        do_speedtest = False
        self.mac_address = ":".join(("%012X" % mac)[i: i + 2] for i in range(0, 12, 2))
        if not self.mac_address:
            self.mac_address = UNKNOWN

        self.hostname = socket.gethostname()
        if not self.hostname:
            self.hostname = UNKNOWN
            self.ip_address = UNKNOWN
        else:
            self.ip_address = socket.gethostbyname(self.hostname)

        if self.connection_status:
            prev_network = self.get_saved_network_details()
            if prev_network == None:
                do_speedtest = True
            else:
                if prev_network.ip_address != self.ip_address:
                    do_speedtest = True
                if check_time_delta(prev_network.time_now):
                    do_speedtest = True
            if do_speedtest:
                self.speed_test = speedtest.Speedtest(secure=1)
                self.time_now = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                self.down_speed = round(round(self.speed_test.download()) / 1048576, 2)
                self.up_speed = round(round(self.speed_test.upload()) / 1048576, 2)
            else:
                self.time_now = prev_network.time_now
                self.speed_test = prev_network.speed_test
                self.up_speed = prev_network.speed_test
                self.down_speed = prev_network.down_speed
        else:
            self.down_speed = UNKNOWN
            self.up_speed = UNKNOWN
        self.addresses = psutil.net_if_addrs()
        self.stats = psutil.net_if_stats()
        self.connected_interface = UNKNOWN
        prefixes = ["169.254", "127."]
        for intface, addr_list in self.addresses.items():
            if any(
                    getattr(addr, "address").startswith(tuple(prefixes))
                    for addr in addr_list
            ):
                continue
            elif intface in self.stats and getattr(self.stats[intface], "isup"):
                self.connected_interface = intface
        if speedtest:
            self.save_network_details()

    def fill_network_info(self, json: dict):
        json["mac_address"] = self.mac_address
        json["ip_address"] = self.ip_address
        json["hostname"] = self.hostname
        json["connected_interface"] = self.connected_interface
        json["connection_status"] = self.connection_status
        json["down_speed"] = self.down_speed
        json["up_speed"] = self.up_speed
        json["time_now"] = self.time_now

    def save_network_details(self) -> None:
        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../data/network.pickle'), 'wb') as handle:
            pickle.dump(self, handle, protocol=pickle.HIGHEST_PROTOCOL)

    @staticmethod
    def get_saved_network_details():
        if not os.path.exists(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../data/network.pickle')):
            return None

        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../data/network.pickle'), 'rb') as handle:
            # case where file is not already present
            old_obj = pickle.load(handle)
        return old_obj
