import sys
import time
import logging
from watchdog.observers.polling import PollingObserver
from watchdog.events import FileSystemEventHandler, FileSystemEvent

import subprocess
import os

from .const import FUSE_PATH

class FuseEventHandler(FileSystemEventHandler):
    """Logs all the events captured."""

    def __init__(self, logger: logging.Logger, panel_entity) -> None:
        self.logger = logger
        self.panel_entity = panel_entity

    def on_moved(self, event: FileSystemEvent) -> None:
        what = "directory" if event.is_directory else "file"
        self.logger.info("Moved %s: from %s to %s", what, event.src_path, event.dest_path)

    def on_created(self, event: FileSystemEvent) -> None:
        what = "directory" if event.is_directory else "file"
        self.logger.info("Created %s: %s", what, event.src_path)

        if event.is_directory:
            return

        splitted_path = event.src_path.replace(FUSE_PATH + "/", "").split("/")

        self.logger.info("after replacing: %s", event.src_path.replace(FUSE_PATH+"/", ""))  
        if len(splitted_path) > 2 and splitted_path[0] == "devices":
            if splitted_path[1].isdigit():
                device_id = int(splitted_path[1])
            else:
                self.logger.error("Invalid Device ID in path: %s", event.src_path)    
                return
            
            self.logger.info("Device ID is: %i", device_id)

            if splitted_path[2] == "last_button":
                f = open(event.src_path, "r")
                button = int(f.read(1))
                self.logger.info("Button %s pressed", button)
                self.panel_entity.button_pressed(button)

    def on_deleted(self, event: FileSystemEvent) -> None:
        what = "directory" if event.is_directory else "file"
        self.logger.info("Deleted %s: %s", what, event.src_path)

    def on_modified(self, event: FileSystemEvent) -> None:
        what = "directory" if event.is_directory else "file"
        self.logger.info("Modified %s: %s", what, event.src_path)

        if event.is_directory:
            return

        splitted_path = event.src_path.replace(FUSE_PATH + "/", "").split("/")
        self.logger.info("after replacing: %s", event.src_path.replace(FUSE_PATH + "/", ""))  
        if len(splitted_path) > 2 and splitted_path[0] == "devices":
            if splitted_path[1].isdigit():
                device_id = int(splitted_path[1])
            else:
                self.logger.error("Invalid Device ID in path: %s", event.src_path)    
                return
            
            self.logger.info("Device ID is: %i", device_id)

            if splitted_path[2] == "last_button":
                f = open(event.src_path, "r")
                button = int(f.read(1))
                self.logger.info("Button %s pressed", button)
                self.panel_entity.button_pressed(button)

    def on_closed(self, event: FileSystemEvent) -> None:
        self.logger.info("Closed file: %s", event.src_path)

    def on_opened(self, event: FileSystemEvent) -> None:
        self.logger.info("Opened file: %s", event.src_path)

# if __name__ == "__main__":
# logging.basicConfig(level=logging.INFO,
#                     format='%(asctime)s - %(message)s',
#                     datefmt='%Y-%m-%d %H:%M:%S')

# path = sys.argv[1] if len(sys.argv) > 1 else '.'
# fuse_path = "/home/imixiru/work/test"

def StartMonitoringFuse(logger: logging.Logger, panel_entity):
    event_handler = FuseEventHandler(logger, panel_entity)
    observer = PollingObserver()
    observer.schedule(event_handler, FUSE_PATH, recursive=True)
    observer.start()
    logger.info("Observer started")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()