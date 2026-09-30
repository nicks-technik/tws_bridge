import os
from typing import Callable
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileCreatedEvent
from loguru import logger

class OrderFileHandler(FileSystemEventHandler):
    """Handler to process file system events for new order files."""
    
    def __init__(self, callback: Callable[[str], None]):
        self.callback = callback

    def on_created(self, event):
        if event.is_directory:
            return
        
        # Check if file ends with .json
        if event.src_path.lower().endswith(".json"):
            logger.debug(f"Detected new JSON file: {event.src_path}")
            self.callback(event.src_path)

class FolderMonitor:
    """Wrapper to manage Watchdog observer monitoring the queue directory."""
    
    def __init__(self, watch_dir: str, callback: Callable[[str], None]):
        self.watch_dir = watch_dir
        self.handler = OrderFileHandler(callback)
        self.observer = Observer()

    def start(self):
        logger.info(f"Starting directory monitor on: {self.watch_dir}")
        self.observer.schedule(self.handler, self.watch_dir, recursive=False)
        self.observer.start()

    def stop(self):
        logger.info("Stopping directory monitor")
        self.observer.stop()
        self.observer.join()
