import datetime

#Dir
from enums import TradeStateTypes

# Pydantic
from typing import Optional, List
from pydantic import BaseModel, Field


class PnlFilterBody(BaseModel):
    accountID: str
    ids: Optional[List[str]] = None
    state: Optional[TradeStateTypes] = Field(TradeStateTypes.ALL.value,
                                             description="State of the trades you want to return")
    instrument: Optional[str] = None
    count: Optional[int] = Field(50, le=500, description="Max number of trades to return")
    day: Optional[str] = Field(datetime.datetime.now(), description="The day you are looking for")
    start: Optional[str] = Field(None, description="The start date")
    end: Optional[str] = Field(None, description="The end date")
    beforeID: Optional[str] = None

