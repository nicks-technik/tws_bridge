import os
from pydantic import BaseModel, Field, field_validator

class Settings(BaseModel):
    """Configuration settings for the NinjaTrader to TWS Order Bridge."""
    
    TWS_HOST: str = Field(default_factory=lambda: os.getenv("TWS_HOST", "127.0.0.1"))
    TWS_PORT: int = Field(default_factory=lambda: int(os.getenv("TWS_PORT", "7497")))
    TWS_CLIENT_ID: int = Field(default_factory=lambda: int(os.getenv("TWS_CLIENT_ID", "1")))
    WATCH_DIR: str = Field(default_factory=lambda: os.getenv("WATCH_DIR", ""), validate_default=True)
    PROCESSED_DIR: str = Field(default="")
    ERROR_DIR: str = Field(default="")
    LOG_FILE: str = Field(default="")

    @field_validator("WATCH_DIR")
    @classmethod
    def validate_watch_dir(cls, v: str) -> str:
        if not v:
            raise ValueError("WATCH_DIR is required and cannot be empty")
        if not os.path.exists(v):
            raise ValueError(f"WATCH_DIR path does not exist: {v}")
        return v

    def model_post_init(self, __context) -> None:
        if self.WATCH_DIR:
            if not self.PROCESSED_DIR:
                self.PROCESSED_DIR = os.path.join(self.WATCH_DIR, "processed")
            if not self.ERROR_DIR:
                self.ERROR_DIR = os.path.join(self.WATCH_DIR, "error")
            if not self.LOG_FILE:
                self.LOG_FILE = os.path.join(self.WATCH_DIR, "bridge.log")
            
            # Ensure subdirectories exist
            os.makedirs(self.PROCESSED_DIR, exist_ok=True)
            os.makedirs(self.ERROR_DIR, exist_ok=True)
