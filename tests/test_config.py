import os
import pytest
from pydantic import ValidationError
from tws_bridge.config import Settings

def test_settings_watch_dir_required():
    # WATCH_DIR must be specified
    with pytest.raises(ValidationError):
        Settings()

def test_settings_load_from_env(tmp_path):
    watch_dir = tmp_path / "queue"
    watch_dir.mkdir()
    
    os.environ["WATCH_DIR"] = str(watch_dir)
    os.environ["TWS_PORT"] = "4002"
    os.environ["TWS_HOST"] = "192.168.1.100"
    
    try:
        settings = Settings()
        assert settings.WATCH_DIR == str(watch_dir)
        assert settings.TWS_PORT == 4002
        assert settings.TWS_HOST == "192.168.1.100"
        
        # Verify defaults are set correctly based on WATCH_DIR
        assert settings.PROCESSED_DIR == str(watch_dir / "processed")
        assert settings.ERROR_DIR == str(watch_dir / "error")
        assert settings.LOG_FILE == str(watch_dir / "bridge.log")
    finally:
        del os.environ["WATCH_DIR"]
        del os.environ["TWS_PORT"]
        del os.environ["TWS_HOST"]
