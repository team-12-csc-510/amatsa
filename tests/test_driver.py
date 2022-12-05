"""Tests on driver code"""
import json
from datetime import datetime
from typing import Dict

from mock import MagicMock, patch

from src import driver


@patch("pyJoules.energy_meter.EnergyMeter.start")
@patch("pyJoules.energy_meter.EnergyMeter.stop")
def test_data_collection(stop: MagicMock, start: MagicMock):
    success = True
    data: Dict = {}
    start.return_value = {}
    stop.return_value = {}
    try:
        if not driver.CollectMetrics(data):
            success = False
    except ValueError:  # pylint: disable=bare-except
        success = False
    assert success, "Failed to collect metrics"


@patch("pyJoules.energy_meter.EnergyMeter.start")
@patch("pyJoules.energy_meter.EnergyMeter.stop")
def test_json_validation(stop: MagicMock, start: MagicMock):
    success = True
    client_json = {}
    start.return_value = {}
    stop.return_value = {}
    try:
        # dummy meta-data fields
        version = "1.0"
        client_json["metadata"] = {
            "version": version,
            "time": datetime.utcnow().isoformat() + "Z",
        }

        if driver.CollectMetrics(client_json):
            _ = json.loads(json.dumps(client_json, indent=2))
            print(json.dumps(client_json, indent=2))

    except ValueError:  # pylint: disable=bare-except
        success = False
    assert success, "Invalid JSON"
