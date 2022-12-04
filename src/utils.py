"""File contains util methods used by all modules"""
import json
import os
from datetime import datetime

import yaml

from aws.client.ses import SES  # type: ignore
from config.threshold import AlarmThreshold, AlarmType  # type: ignore


def size_in_gb(byte) -> int:
    return round(byte / 1024**3, 2)


def fire_alarm(alarm_type: AlarmType):
    ses_object = SES(
        recipient=[os.environ["TEST_RECEIVER1"], os.environ["TEST_RECEIVER2"]]
    )
    if alarm_type is AlarmType.DISK:
        ses_object.subject = f"Caution! Disk usage {AlarmThreshold.DISK.value}%"
        ses_object.body_text = (
            f"Your disk usage has reached "
            f"the threshold {AlarmThreshold.DISK.value}%"
        )
        ses_object.heading = (
            f"Your disk usage has reached "
            f"the threshold usage set {AlarmThreshold.DISK.value}%"
        )

    elif alarm_type is AlarmType.SYSTEM:
        ses_object.subject = f"Caution! CPU usage {AlarmThreshold.SYSTEM.value}%"
        ses_object.body_text = (
            f"Your CPU usage has reached "
            f"the threshold {AlarmThreshold.SYSTEM.value}%"
        )
        ses_object.heading = (
            f"Your CPU usage has reached "
            f"the threshold usage set {AlarmThreshold.SYSTEM.value}%"
        )
    ses_object.send_mail()


def get_config() -> dict:
    with open(
        os.path.dirname(os.path.realpath(__file__)) + "/config/amatsa-client.yml",
        "r",
        encoding="utf-8",
    ) as file:
        config = yaml.safe_load(file)
    return config


def check_time_delta(old_time: str) -> bool:
    time_now = datetime.now()
    time_as_datetime = datetime.strptime(old_time, "%d/%m/%Y %H:%M:%S")
    if (time_now - time_as_datetime).total_seconds() > 900:
        return True
    else:
        return False


def dump_list_to_json(lst: list):
    json_list = []
    for element in lst:
        json_list.append(json.dumps(element.__dict__))
    return json_list
