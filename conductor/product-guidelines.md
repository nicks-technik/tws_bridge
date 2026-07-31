# Product Guidelines

## Development Guidelines
- **Language Stack:**
  - C# (for NinjaTrader 8 indicator/strategy)
  - Python 3.11+ (for TWS monitor and order router)
- **Environment Management:** Python dependencies must be managed using the modern `uv` manager.

## Design & Architecture Guidelines
- **Stateless File Queue:** JSON files are written dynamically by NinjaTrader. The monitor is the sole processor of these files. Once processed, files are moved, avoiding race conditions or reprocessing.
- **Directory Layout:**
  - `queue/` - Incoming orders written by NinjaTrader.
  - `processed/` - Archive of successfully sent orders.
  - `error/` - Failed orders (failed validation, missing parameters, etc.).
- **File Locking Safety:** NinjaTrader must release locks immediately on writing. The Python script should handle file access retries to avoid reading half-written or locked files.

## Error Handling & Reliability
- **TWS API Connectivity:** If connection to TWS is lost:
  - Stop processing the queue.
  - Keep files in `queue/`.
  - Continuously try to reconnect.
  - Log error status with high visibility.
- **Malformed JSON Handling:** If a file in the queue cannot be parsed:
  - Move it immediately to `error/` to prevent blockages.
  - Log the exception details to the log file.

## Logging & Monitoring
- **Log Level:** INFO by default, DEBUG for troubleshooting TWS message flows.
- **Output:** Both console output and standard log file output.
- **Format:** `[TIMESTAMP] [LEVEL] [MODULE] - MESSAGE`.
