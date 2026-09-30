import os
import time
from watchdog.events import FileCreatedEvent
from tws_bridge.monitor import OrderFileHandler

def test_file_handler_triggers_on_json(tmp_path):
    processed_files = []
    
    def mock_callback(filepath):
        processed_files.append(filepath)
        
    handler = OrderFileHandler(callback=mock_callback)
    
    # Simulate a JSON file creation event
    json_path = tmp_path / "order_1.json"
    json_event = FileCreatedEvent(str(json_path))
    handler.on_created(json_event)
    
    assert str(json_path) in processed_files

def test_file_handler_ignores_non_json(tmp_path):
    processed_files = []
    
    def mock_callback(filepath):
        processed_files.append(filepath)
        
    handler = OrderFileHandler(callback=mock_callback)
    
    # Simulate a text file creation event
    txt_path = tmp_path / "order_1.txt"
    txt_event = FileCreatedEvent(str(txt_path))
    handler.on_created(txt_event)
    
    assert len(processed_files) == 0
