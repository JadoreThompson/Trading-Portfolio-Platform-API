from enums import TradeStatusTypes, IntervalTypes

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class BalanceRequest(BaseModel):
    account_id: str


class TradeQueryParams(BaseModel):
    account_id: str
    trade_open_time: Optional[str] = None
    trade_close_time: Optional[str] = None
    symbol: Optional[str] = None


class RiskRatioRequest(BaseModel):
    start: datetime
    end: datetime
    interval: IntervalTypes = Field(default='weekly', description="The interval used for performance check. Defaults to weekly")


# Objects
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
