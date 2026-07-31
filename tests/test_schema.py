import pytest
from pydantic import ValidationError
from tws_bridge.schema import OrderPayload

def test_valid_market_order():
    payload = {
        "Action": "BUY",
        "OrderType": "MARKET",
        "Symbol": "FDAX",
        "Quantity": 1
    }
    order = OrderPayload(**payload)
    assert order.Action == "BUY"
    assert order.OrderType == "MARKET"
    assert order.Symbol == "FDAX"
    assert order.Quantity == 1

def test_valid_limit_order_with_brackets():
    payload = {
        "Action": "SELL",
        "OrderType": "LIMIT",
        "LimitPrice": 16000.5,
        "TP": 16100.0,
        "SL": 15950.0,
        "ATR": 15.0,
        "Symbol": "FDXM",
        "Quantity": 2
    }
    order = OrderPayload(**payload)
    assert order.Action == "SELL"
    assert order.OrderType == "LIMIT"
    assert order.LimitPrice == 16000.5
    assert order.TP == 16100.0
    assert order.SL == 15950.0
    assert order.ATR == 15.0
    assert order.Symbol == "FDXM"
    assert order.Quantity == 2

def test_invalid_action():
    with pytest.raises(ValidationError):
        OrderPayload(Action="HOLD", OrderType="MARKET", Symbol="FDAX", Quantity=1)

def test_missing_limit_price_for_limit_order():
    with pytest.raises(ValidationError):
        OrderPayload(Action="BUY", OrderType="LIMIT", Symbol="FDAX", Quantity=1)

def test_negative_quantity():
    with pytest.raises(ValidationError):
        OrderPayload(Action="BUY", OrderType="MARKET", Symbol="FDAX", Quantity=0)

def test_atr_validation_valid():
    payload = {
        "Action": "BUY",
        "OrderType": "LIMIT",
        "LimitPrice": 16000.0,
        "TP": 16030.0,
        "SL": 15985.0,
        "ATR": 15.0,
        "Symbol": "FDAX",
        "Quantity": 1
    }
    order = OrderPayload(**payload)
    assert order.ATR == 15.0

def test_atr_validation_too_far_tp():
    payload = {
        "Action": "BUY",
        "OrderType": "LIMIT",
        "LimitPrice": 16000.0,
        "TP": 16300.0,
        "SL": 15985.0,
        "ATR": 15.0,
        "Symbol": "FDAX",
        "Quantity": 1
    }
    with pytest.raises(ValidationError) as exc_info:
        OrderPayload(**payload)
    assert "TP is too far" in str(exc_info.value)

