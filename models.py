from enum import Enum
from typing import Optional, List
from pydantic import BaseModel, Field


"""
Enums
"""
class OrderSide(str, Enum):
    BUY = 'buy'
    SELL = 'sell'


"""
Models
"""
class AccountBody(BaseModel):
    account_id: str = Field(max_length=250)


class AllOrderBody(AccountBody):
    status: str = Field("open", description="Order status to be queried. open, closed or all. Defaults to open.")
    limit: int = Field(50, ge=1, le=500, description="Max number of orders to retrieve")
    after: Optional[str] = Field(None)
    until: Optional[str] = Field(None)
    direction: str = Field("desc", description="Chronological order. asc or desc")
    nested: Optional[bool] = Field(False,
                                   description="If true, the result will roll up multi-leg orders under the legs field of primary order.")
    side: Optional[OrderSide] = None
    symbols: Optional[List[str]] = Field(None, description="Comma separated list of symbols. (BTCUSDT, LTCUSDT)")
