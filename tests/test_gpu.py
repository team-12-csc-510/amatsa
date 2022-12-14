"""Tests for the Disk module"""
from src.gpu import GPUdata


def test_gpu_init():
    success = True
    try:
        _ = GPUdata()
        if _ is False:
            raise TypeError
    except TypeError:  # pylint: disable=bare-except
        success = False
    assert success, "Failed to initialize GPUdata()"


def test_gpu_datatype():
    success = True
    try:
        gpu = GPUdata()
        data = gpu.retrieve_gpu_info()
        if data is False:
            raise TypeError
    except TypeError:  # pylint: disable=bare-except
        print("Failed to collect Data metrics")
        success = False
    num = (float, int)
    data_types = {
        "gpu_name": str,
        "uuid": str,
        "serial_number": num,
        "load": num,
        "total_memory": num,
        "memory_used": num,
        "memory_free": num,
    }
    for each in data:
        for field in each.keys():
            if not isinstance(each[field], data_types[field]):  # type: ignore
                print(
                    f"For gpu data '{field}', "
                    f"type should be {data_types[field]}, "
                    f"not {type(each[field])}"
                )
                success = False
    assert success


def test_disk_values():
    success = True
    try:
        gpu = GPUdata()
        data = gpu.retrieve_gpu_info()
        if data is False:
            raise TypeError
    except TypeError:  # pylint : bare-except
        print("Failed to collect Data metrics")
        success = False
    fields = ["total_memory", "memory_used", "memory_free", "load"]
    for each in data:
        for each_field in fields:
            if each[each_field] < 0:
                print(f"For gpu data '{each_field}', value cannot be negative")
                success = False
    assert success
