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
