#!/usr/bin/python
"""
This module fetches network information and returns a JSON with the network info data
"""
import logging
import sys
import time

# pylint: disable=consider-using-f-string
import psutil


class Process:
    """Class to deal with individual processes"""

    def __init__(self, process_id: int) -> None:
        self.process_id: int = process_id
        self.memory_percent: float = 0.0
        self.memory_info: dict = dict()
        self.cpu_percent: float = 0.0
        self.process_name: str = ""

    def get_process_detail(self):
        try:
            process = psutil.Process(self.process_id)
            self.cpu_percent = process.cpu_percent()
            self.memory_percent = process.memory_percent()
            self.memory_info = process.memory_info()
            self.process_name = process.name()
            return process
        except Exception as e:
            logging.info(e, "occurred.")

    def update_cpu(self, proc):
        self.cpu_percent = proc.cpu_percent()


class ProcessMeta:
    """parent class to handle multiple process data"""

    process_list: list[Process] = []

    def __init__(self) -> None:
        self.top_cpu: list[Process] = list()
        self.top_memory: list[Process] = list()
        self.create_lists()

    def create_lists(self):
        process_psutil_list = []
        for proc in psutil.process_iter():
            try:
                if psutil.pid_exists(proc.pid):
                    process_detail = Process(proc.pid)
                    process_psutil_list.append(process_detail.get_process_detail())
                    self.process_list.append(process_detail)
            except psutil.AccessDenied:
                logging.info(sys.exc_info()[0], "occurred.")

        idx = 0
        time.sleep(0.1)
        for proc in self.process_list:
            if process_psutil_list[idx] is not None:
                proc.update_cpu(process_psutil_list[idx])
                idx += 1

        memory_sorted_list = sorted(
            self.process_list, key=lambda x: x.memory_percent, reverse=True
        )
        self.top_memory = memory_sorted_list[:5]
        cpu_sorted_list = sorted(
            self.process_list, key=lambda x: x.cpu_percent, reverse=True
        )
        self.top_cpu = cpu_sorted_list[:5]

    def retrieve_process_info(self):
        """Retrieve process  information, format and return it"""
        data = {}
        data["high_cpu_processes"] = []
        data["high_memory_processes"] = []
        for x in self.top_cpu:
            each_cpu = {
                "process_name": x.process_name,
                "process_id": x.process_id,
                "memory_percent": x.cpu_percent,
                "cpu_percent": x.memory_percent,
                "memory_info": x.memory_info,
            }
            data["high_cpu_processes"].append(each_cpu)

        for x in self.top_memory:
            each_memory = {
                "process_name": x.process_name,
                "process_id": x.process_id,
                "memory_percent": x.cpu_percent,
                "cpu_percent": x.memory_percent,
                "memory_info": x.memory_info,
            }
            data["high_memory_processes"].append(each_memory)

        return data["high_memory_processes"], data["high_cpu_processes"]
