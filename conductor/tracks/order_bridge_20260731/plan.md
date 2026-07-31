# Implementation Plan - Order Bridge Setup

This plan details the steps required to implement the NinjaTrader to TWS order bridge.

## Phase 1: Environment and Core Data Models

- [ ] Task: Project and Configuration Setup
  - [ ] Initialize Python environment using `uv init` and add dependencies (`ib_insync`, `watchdog`, `pydantic`, `loguru`, `pytest`).
  - [ ] Write unit tests for the configuration manager to verify loading settings from environment variables/config file.
  - [ ] Implement configuration module to load and validate TWS port, watch directory path, and log file location.
- [ ] Task: JSON Schema and Payload Validation
  - [ ] Write unit tests for JSON parsing and schema validation covering valid, invalid, and missing fields.
  - [ ] Implement Pydantic schema representing the NinjaTrader order payload (`Action`, `OrderType`, `LimitPrice`, `TP`, `SL`, `ATR`, `Symbol`, `Quantity`).
  - [ ] Write validation tests for ATR-based limits (rejecting orders if TP/SL distance deviates radically from ATR).
  - [ ] Implement ATR-based bounds validator for SL and TP inputs.
- [ ] Task: Conductor - User Manual Verification 'Phase 1: Environment and Core Data Models' (Protocol in workflow.md)

## Phase 2: Directory Monitor and Queue System

- [ ] Task: Watchdog Directory Monitor
  - [ ] Write unit tests for file event handler simulating directory creation and modification events.
  - [ ] Implement Watchdog-based monitor observing the queue folder and triggers parser.
- [ ] Task: Queue Processing and File Safety
  - [ ] Write tests verifying file-lock handling and retrying partially written files.
  - [ ] Implement file access safety loop with retries before parsing.
  - [ ] Write tests verifying archiving logic (successful files moved to `processed/`, failed files moved to `error/`).
  - [ ] Implement file mover utility.
- [ ] Task: Conductor - User Manual Verification 'Phase 2: Directory Monitor and Queue System' (Protocol in workflow.md)

## Phase 3: Interactive Brokers TWS Integration

- [ ] Task: TWS API Connection and Reconnection
  - [ ] Write tests for connection lifecycle and reconnection manager.
  - [ ] Implement `ib_insync` TWS connection manager with automatic reconnection loop and status reporting.
- [ ] Task: Contract Mapping and Order Execution
  - [ ] Write unit tests mapping FDAX, FDXM, and FDXX symbols to standard IB Future contracts.
  - [ ] Implement Symbol contract mapper.
  - [ ] Write unit tests verifying creation of Market, Limit, and Bracket orders (OCA groups) under `ib_insync`.
  - [ ] Implement order submission logic in the bridge service.
- [ ] Task: Conductor - User Manual Verification 'Phase 3: Interactive Brokers TWS Integration' (Protocol in workflow.md)

## Phase 4: NinjaTrader Export & End-to-End Test

- [ ] Task: End-to-End Integration Validation
  - [ ] Write an integration test suite simulating full flow: writing a JSON order file, detecting it, submitting it to a mock TWS API, and verifying log logs and file placement.
  - [ ] Implement a command line test utility script that prints system diagnostics and tests connectivity.
  - [ ] Create a NinjaScript C# skeleton snippet for NinjaTrader 8 demonstrating how to save the JSON file correctly.
- [ ] Task: Conductor - User Manual Verification 'Phase 4: NinjaTrader Export & End-to-End Test' (Protocol in workflow.md)
