from src.utils import size_in_gb, get_config, check_time_delta
import datetime


def test_size_in_gb():
    success = True
    try:
        size_in_gb(1024000)
    except Exception as e:
        print(e)
        success = False
    assert success, "did not convert correctly"


def test_get_config():
    success = True
    try:
        val = get_config()
    except Exception as e:
        print(e)
        success = False
    assert success, "Wrong config returned"


def test_check_time_delta():
    success = True
    time_now = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    try:
        check_time_delta(time_now)
    except Exception as e:
        print(e)
        success = False
    assert success, "Time delta failed"
