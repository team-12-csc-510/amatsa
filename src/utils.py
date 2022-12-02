"""File contains util methods used by all modules"""
import os

from aws.client.ses import SES
from config.threshold import AlarmThreshold, AlarmType


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
