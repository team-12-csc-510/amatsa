import os

from src.file_monitoring import FileMonitoring


def test_file_init():
    success = True
    try:
        _ = FileMonitoring()
    except Exception as e:
        print(e)
        success = False
    assert success, "Failed to initialize monitoring"


def test_get_file():
    success = True
    try:
        monitor = FileMonitoring()
        monitor.get_filename()
    except Exception as e:
        print(e)
        success = False
    assert success, "Failed to get file"


def test_start_file_monitoring():
    success = True
    try:
        monitor = FileMonitoring()
        monitor.start_file_monitoring()
    except Exception as e:
        print(e)
        success = False
    assert success, "Failed to start file monitoring"


def test_read_data():
    success = True
    try:
        f = open("file_monitoring_data", "w+")
        monitor = FileMonitoring()
        monitor.read_data()
        os.remove("file_monitoring_data")
    except Exception as e:
        print(e)
        success = False
    assert success, "Failed to read data"


def test_FolderMonitoring_init():
    success = True
    try:
        _ = FileMonitoring.FolderMonitoring("file_monitoring_data")
    except Exception as e:
        print(e)
        success = False
    assert success, "Failed to initialize folder monitoring"
