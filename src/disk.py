"""This module fetches disk information and returns a JSON with the disk data"""
import logging
import re
import time

import psutil

from src.config.threshold import AlarmThreshold, AlarmType  # type: ignore
from src.system import System
from src.utils import fire_alarm, size_in_gb  # type: ignore


class Disk:
    """Class to fetch, format and return disk information"""

    def __init__(self):
        self.data = {}
        self.sys = System()

    def check_attr(self, attr, val):
        """
        Check whether attribute for object present, if present, call and return data
        """
        try:
            val = getattr(attr, val)
        except (AttributeError, ValueError) as e:
            logging.error(
                time, str(e), "occurred while trying to get disk attribute-" + val
            )
            val = None
        return val

    def format_darwin(self, data):
        """Format disk data for macOS,
        summarize all partitions into the disk it belongs to

        :param data : disk data sent to be formatted
        """
        disk_nums = [[] for i in range(len(data["disk"]))]
        for i in range(0, len(disk_nums)):
            result = re.search(r"/dev/disk(\d+)s", data["disk"][i]["name"])
            if result is not None:
                result = int(result.group(0).replace("/dev/disk", "").replace("s", ""))
                data["disk"][i]["number"] = result
                disk_nums[result].append(data["disk"][i])
        res = [ele for ele in disk_nums if ele != []]

        final_disk = []
        for each_disk in res:
            # print(each_disk)
            total_size = each_disk[0]["total_size"]
            used = each_disk[0]["used"]
            free = each_disk[0]["free"]
            name = "/dev/disk" + str(each_disk[0]["number"])
            type_disk = each_disk[0]["type"]
            percentage = round((used / total_size) * 100, 2)

            summed_disk = {
                "name": name,
                "type": type_disk,
                "total_size": total_size,
                "used": used,
                "free": free,
                "percentage": percentage,
            }

            final_disk.append(summed_disk)
        return final_disk

    def retrieve_disk_info(self):
        """Retrive disk information, format and return it"""
        par = psutil.disk_partitions()
        self.data["disk"] = []
        for x in par:
            dsk = psutil.disk_usage(x.mountpoint)
            each_disk = {}

            each_disk["name"] = self.check_attr(x, "device")
            each_disk["type"] = self.check_attr(x, "fstype")
            each_disk["total_size"] = size_in_gb(self.check_attr(dsk, "total"))
            each_disk["used"] = size_in_gb(self.check_attr(dsk, "used"))
            each_disk["free"] = size_in_gb(self.check_attr(dsk, "free"))
            each_disk["percentage"] = self.check_attr(dsk, "percent")

            self.data["disk"].append(each_disk)

        if self.sys.platform_name == "Darwin":
            self.data["disk"] = self.format_darwin(self.data)

        for disk in self.data["disk"]:
            if disk["percentage"] >= AlarmThreshold.DISK.value:
                fire_alarm(AlarmType.DISK)
        return self.data["disk"]
