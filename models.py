from enums import TradeStatusTypes

from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class TradeRequest(BaseModel):
    account_id: str
    trade_open_time: Optional[str] = None
    trade_close_time: Optional[str] = None
    day: Optional[str] = None
    symbol: Optional[str] = None


class TradeObject(BaseModel):
    trade_id: Optional[str] = None
    order_id: Optional[str] = None
    symbol: Optional[str] = None
    trade_open_time: Optional[datetime] = None
    trade_close_time: Optional[datetime] = None
    starting_balance: Optional[float] = None
    trade_open_price: Optional[float] = None
    trade_close_price: Optional[float] = None
    closing_balance: Optional[float] = None
    realised_pnl: Optional[float] = None
    trade_status: Optional[TradeStatusTypes] = None
