"""This module fetches GPU information and returns a JSON with the GPU data"""
import logging
import time

import GPUtil  # type: ignore


class GPUdata:
    """Class to fetch, format and return GPU information"""

    gpudata = None

    def __init__(self):
        self.gpudata = []

    def check_attr(self, attr, val):
        """Return the value of indicated attribute"""
        try:
            val = getattr(attr, val)
        except (AttributeError, ValueError) as e:
            logging.error(
                time, str(e) + "occurred while trying to get GPU attribute-" + val
            )
            val = None
        return val

    def retrieve_gpu_info(self):
        """retrieve the GPU information like name, uuid,serial_number
        load, total_memory, memory_free in the gpu dictionary."""
        gpu = GPUtil.getGPUs()
        for x in gpu:
            gpu = {}

            gpu["name"] = self.check_attr(x, "gpu_name")
            gpu["uuid"] = self.check_attr(x, "uuid")
            gpu["serial_number"] = self.check_attr(x, "serial")
            gpu["load"] = self.check_attr(x, "load")
            gpu["total_memory"] = self.check_attr(x, "memoryTotal")
            gpu["memory_used"] = self.check_attr(x, "memoryUsed")
            gpu["memory_free"] = self.check_attr(x, "memoryFree")

            self.gpudata.append(gpu)
        return self.gpudata
