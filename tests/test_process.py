from src.process import Process, ProcessMeta

"""Tests for the Process Module"""
from src.disk import Disk


def test_process_init():
    success = True
    try:
        _ = Process(1)
    except Exception as e:
        success = False
    assert success, "Failed to initialize Process()"


def test_process_detail():
    success = True
    try:
        process = Process(1)
        data = process.get_process_detail()
    except Exception as e:
        print("Failed to collect process details", e)
        success = False
    assert success


def test_update_cpu():
    success = True
    try:
        disk = Disk()
        data = disk.retrieve_disk_info()
        data.update_cpu()
    except Exception as e:
        print("Failed to collect Data metrics", e)
    assert success


def test_process_meta():
    success = True
    try:
        _ = ProcessMeta()
    except Exception as e:
        success = False
    assert success, "Failed to initialize ProcessMeta()"


def test_retrieve_info():
    success = True
    try:
        meta = ProcessMeta()
        meta.retrieve_process_info()
    except Exception as e:
        success = False
    assert success, "Failed to retrieve information in the desired format"
