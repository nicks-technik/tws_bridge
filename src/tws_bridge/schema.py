from typing import Optional, Literal
from pydantic import BaseModel, Field, model_validator

class OrderPayload(BaseModel):
    """Pydantic schema representing the NinjaTrader order payload."""
    
    Action: Literal["BUY", "SELL"]
    OrderType: Literal["LIMIT", "MARKET"]
    LimitPrice: Optional[float] = None
    TP: Optional[float] = None
    SL: Optional[float] = None
    ATR: Optional[float] = None
    Symbol: str
    Quantity: int = Field(..., ge=1)

    @model_validator(mode="after")
    def validate_limit_price(self) -> "OrderPayload":
        if self.OrderType == "LIMIT" and (self.LimitPrice is None or self.LimitPrice <= 0):
            raise ValueError("LimitPrice must be a positive float when OrderType is LIMIT")
        
        if self.ATR and self.ATR > 0:
            max_mult = 15.0
            if self.OrderType == "LIMIT" and self.LimitPrice:
                if self.TP and abs(self.TP - self.LimitPrice) > max_mult * self.ATR:
                    raise ValueError(f"TP is too far from LimitPrice (> {max_mult} * ATR)")
                if self.SL and abs(self.SL - self.LimitPrice) > max_mult * self.ATR:
                    raise ValueError(f"SL is too far from LimitPrice (> {max_mult} * ATR)")
            elif self.OrderType == "MARKET":
                if self.TP and self.SL and abs(self.TP - self.SL) > max_mult * 2 * self.ATR:
                    raise ValueError(f"TP/SL distance is too far (> {max_mult * 2} * ATR)")
        return self
