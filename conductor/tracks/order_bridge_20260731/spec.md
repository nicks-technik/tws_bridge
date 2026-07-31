# Track Specification - Order Bridge

## Goal
Implement a lightweight local file-based bridge that processes order JSON files exported by NinjaTrader strategies and routes them to Interactive Brokers (IB) Trader Workstation (TWS) using a Python monitor service.

## Functional Scope
1. **Configurable Directory Monitor:**
   - Monitor a specified local directory for incoming `.json` order files.
   - Support safe read retries (handling partial writes/file locking by NinjaTrader).
   - Move successfully processed files to a `processed/` directory.
   - Move failed/malformed files to an `error/` directory.
2. **Order Payload Validation:**
   - Parse order JSON including fields: `action`, `order_type`, `limit_price`, `tp`, `sl`, `atr`, `symbol`, `quantity`.
   - Implement parameter limits (ATR-based SL/TP validation sanity check).
3. **Interactive Brokers TWS Integration:**
   - Establish and maintain TWS API connection via `ib_insync`.
   - Map symbols specifically for Eurex Futures: `FDAX`, `FDXM` (Mini-DAX), and `FDXX` (Micro-DAX).
   - Execute Market, Limit, and Bracket (Entry + TP/SL OCA group) orders.
   - Automatically reconnect to TWS on disconnection.

## Architecture
```
[NinjaTrader 8 Strategy] --Writes JSON--> [local queue/ folder]
                                                |
                                         (File detection)
                                                v
                                       [Python Monitor]
                                                |
                                        (Pydantic Validation)
                                                v
                                         [ib_insync API]
                                                |
                                                v
                                           [Local TWS]
```

## Testing Strategy
- Unit tests with `pytest` for JSON parser, config loader, and order translation.
- Mocking the IB API connection to verify contract mapping and bracket order creation.
- End-to-end integration test using mock JSON files to simulate NinjaTrader triggers.
