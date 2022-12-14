"""Tests for the Network module"""
import random
import re

from src.network import Network


def test_network_init():
    success = True
    try:
        _ = Network()
        _.mac_address = mock_mac_add()
    except Exception as e:
        print(e)
        success = False
    assert success, "Failed to initialize Network()"


def test_network_entries():
    success = True
    json = {}
    try:
        net_obj = Network()
        net_obj.mac_address = mock_mac_add()
        net_obj.get_network_info()
        net_obj.fill_network_info(json)
        for k, v in json.items():
            if isinstance(v, str) and str in (None, "unknown"):
                print(f"Value [{v}] for '{k}' is not expected, expected str.")
                success = False
            else:
                print(f"{k}:{v}, type:{type(v)}")
    except Exception as e:
        print(e)
        success = False
    assert success, "Failed to collect Network info"


def test_network_datatype():
    success = True
    json = {}
    try:
        net_obj = Network()
        net_obj.mac_address = mock_mac_add()
        net_obj.get_network_info()
        net_obj.fill_network_info(json)
    except Exception as e:
        print(e)
        print("Failed to collect Network metrics")
        success = False
    data_types = {
        "mac_address": str,
        "ip_address": str,
        "hostname": str,
        "connection_status": bool,
        "down_speed": float,
        "up_speed": float,
        "time_now": str,
        "connected_interface": str,
    }
    for k, v in json.items():
        if not isinstance(v, data_types[k]):  # type: ignore
            print(f"For data '{k}', type should be {data_types[k]}, not {type(v[k])}")
            success = False
    assert success


def test_macadd():
    success = True
    json = {}
    try:
        net_obj = Network()
        print(net_obj.mac_address)
        net_obj.mac_address = mock_mac_add()
        print(net_obj.mac_address)
        net_obj.get_network_info()
        net_obj.fill_network_info(json)
        if not re.match(
            r"([0-9a-fA-F]{2}[-:]){5}[0-9a-fA-F]{2}$",
            json["mac_address"],
            re.IGNORECASE,
        ):
            success = False
    except Exception as e:
        print("Invalid Mac address validation", e)
        success = False
    assert success


def mock_mac_add():
    return "02:00:00:%02x:%02x:%02x" % (
        random.randint(0, 255),
        random.randint(0, 255),
        random.randint(0, 255),
    )
