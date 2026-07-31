# Technology Stack

## Languages & Runtimes
- **Python:** 3.12 (managed via `uv`)
- **C# / .NET:** .NET Framework 4.8 (NinjaTrader 8 runtime environment)

## Key Libraries & Frameworks
- **ib_insync (Python):** Pythonic async library for Interactive Brokers API interaction.
- **watchdog (Python):** File system events monitoring library to detect new files in the queue folder.
- **pydantic (Python):** Data validation and settings management using python type annotations to validate JSON order payloads.
- **loguru (Python):** Elegant and robust logging utility.

## Platforms & Environments
- **NinjaTrader 8:** Operating on Windows, executing NinjaScript indicators/strategies to output JSON files.
- **Interactive Brokers TWS / IB Gateway:** Local API server running on port 7497 (TWS paper) or 7496 (TWS live).
- **OS:** Windows 10/11 (Single-user local environment).
