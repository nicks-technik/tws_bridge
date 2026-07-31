# Initial Concept

A system to send orders from NinjaTrader to Interactive Brokers TWS via JSON file export and a python (uv) monitor.

# Product Guide - NinjaTrader to TWS Order Bridge

## Project Overview
This project implements an automated order execution bridge between NinjaTrader and Interactive Brokers Trader Workstation (TWS). NinjaTrader acts as the signal generator, exporting order details to a local JSON file. A Python-based monitor (managed using `uv`) detects the new order files and submits them directly to TWS using the Interactive Brokers API.

## Target Audience & Deployment
- **Deployment:** Single-User Local. Both NinjaTrader and TWS run on the same Windows desktop machine.
- **Goal:** Low-latency local file-based bridge requiring no external web servers or cloud dependencies.

## Architecture & Flow
1. **Signal Generation:** A NinjaTrader custom indicator/strategy exports order metadata as individual JSON files to a designated queue directory.
   - JSON Fields: `Action` (BUY/SELL), `OrderType` (LIMIT/MARKET), `LimitPrice`, `TP` (Take Profit), `SL` (Stop Loss), `ATR` (Average True Range), `Symbol`, `Quantity`.
2. **Directory Monitor:** A Python monitoring script watches the queue directory for new JSON files.
3. **Queue Processing:** When a new JSON file is detected:
   - Read and parse the JSON file.
   - Move the file to `processed/` on successful parsing and execution, or `error/` on failure.
4. **Order Execution:** Python submits the order to TWS via the IB API.
5. **Logging:** Status is written to a local log file (Fire and Forget model).

## Safety & Risk Controls
- **Parameter Validation:** Validate that limit price, quantity, symbol, TP, and SL are present and valid before submitting to TWS.
- **Heartbeat & Connection Checks:** Continuous monitoring of the IB TWS API connection, logging warnings or alerts if TWS is disconnected or not responding.
- **ATR-based Validation:** Check that SL/TP distances are proportional to the exported ATR to prevent accidental extreme values.
