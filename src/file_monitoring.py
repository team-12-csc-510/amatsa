import time
from os import path

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer


class FileMonitoring:

    """
    Monitors changes in a file folder and return file modification/transfer data
    """

    def __init__(self):

        self.filename = "file_monitoring_data"
        self.folder_monitoring = self.FolderMonitoring(self.filename)

    def get_filename(self):
        return self.filename

    def start_file_monitoring(self):
        my_observe = Observer()
        current_path = path.dirname(__file__)
        monitored_folder = "monitored_folder"
        monitored_path = path.abspath(path.join(current_path, "..", monitored_folder))
        my_observe.schedule(self.folder_monitoring, monitored_path, recursive=True)
        my_observe.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            my_observe.stop()
            my_observe.join()

    def read_data(self):
        data_file = open("file_monitoring_data", "r")
        print(data_file.readlines())
        data_file.close()

    class FolderMonitoring(FileSystemEventHandler):
        def __init__(self, filename):
            self.filename = filename

        def get_relative_path(self, my_path):
            current_path = path.dirname(__file__)
            start_path = path.abspath(path.join(current_path, ".."))
            return path.relpath(my_path, start=start_path)

        def on_deleted(self, event):
            file = open(self.filename, "a")
            relative_path = str(self.get_relative_path(event.src_path))
            file.write(relative_path + " " + str(event.event_type) + " " + "\n")
            file.close()

        def on_closed(self, event):
            file = open(self.filename, "a")
            relative_path = str(self.get_relative_path(event.src_path))
            file.write(relative_path + " " + str(event.event_type) + " " + "\n")
            file.close()

        def on_moved(self, event):
            file = open(self.filename, "a")
            relative_path = str(self.get_relative_path(event.src_path))
            file.write(relative_path + " " + str(event.event_type) + " " + "\n")
            file.close()

        def on_created(self, event):
            file = open(self.filename, "a")
            relative_path = str(self.get_relative_path(event.src_path))
            file.write(relative_path + " " + str(event.event_type) + " " + "\n")
            file.close()

    def on_modified(self, event):
        pass

    def on_any_event(self, event):
        pass


if __name__ == "__main__":
    file_monitor = FileMonitoring()
    file_monitor.read_data()
