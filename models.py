from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field

# Local
from enums import OrderType


class Base(BaseModel):
    """
    Base model for all request body models.

    This class serves as a base for other models and configures Pydantic to use enum values
    when serializing or deserializing fields that are based on enums.
    """

    class Config:
        use_enum_values = True


class TradeRequestBody(Base):
    """
    Model representing the request body for filtering trade data.

    Attributes:
        is_active (Optional[bool]): Filters trades by their status (open or closed).
            If True, returns only active (open) trades. If False, returns closed trades.
            Can be set to None to return all trades.

        ticker (Optional[str]): Filters trades by a specific ticker symbol, e.g., "BTC-USDT".
            If not provided, trades for all tickers are returned.

        min_dollar_amount (Optional[float]): Filters trades where the initial investment is greater than or equal to the given value.

        max_dollar_amount (Optional[float]): Filters trades where the initial investment is less than or equal to the given value.

        min_unrealised_pnl (Optional[float]): Filters trades where the unrealised profit and loss (PNL) is greater than or equal to the given value.

        max_unrealised_pnl (Optional[float]): Filters trades where the unrealised profit and loss (PNL) is less than or equal to the given value.

        min_realised_pnl (Optional[float]): Filters trades where the realised profit and loss (PNL) is greater than or equal to the given value.

        max_realised_pnl (Optional[float]): Filters trades where the realised profit and loss (PNL) is less than or equal to the given value.

        min_open_price (Optional[float]): Filters trades where the open price is greater than or equal to the given value.

        max_open_price (Optional[float]): Filters trades where the open price is less than or equal to the given value.

        min_close_price (Optional[float]): Filters trades where the close price is greater than or equal to the given value.

        max_close_price (Optional[float]): Filters trades where the close price is less than or equal to the given value.

        open_start (Optional[datetime]): Filters trades that were opened after the given start date.

        open_end (Optional[datetime]): Filters trades that were opened before the given end date.

        close_start (Optional[datetime]): Filters trades that were closed after the given start date.

        close_end (Optional[datetime]): Filters trades that were closed before the given end date.

        order_type (Optional[OrderType]): Filters trades by order type, either LONG or SHORT.
            If not specified, trades of all types are returned.
    """
    is_active: Optional[bool] = Field(None,
                                      description="Filters through open or close trades; can pass None to return all.")
    ticker: Optional[str] = Field(None,
                                  description="Returns trades on a particular symbol (e.g., BTC-USDT).")
    min_dollar_amount: Optional[float] = Field(None,
                                               description="Returns trades where the initial investment is greater than or equal to this value.")
    max_dollar_amount: Optional[float] = Field(None,
                                               description="Returns trades where the initial investment is less than or equal to this value.")
    min_unrealised_pnl: Optional[float] = Field(None,
                                                description="Returns trades where the unrealised PNL is greater than or equal to this value.")
    max_unrealised_pnl: Optional[float] = Field(None,
                                                description="Returns trades where the unrealised PNL is less than or equal to this value.")
    min_realised_pnl: Optional[float] = Field(None,
                                              description="Returns trades where the realised PNL is greater than or equal to this value.")
    max_realised_pnl: Optional[float] = Field(None,
                                              description="Returns trades where the realised PNL is less than or equal to this value.")
    min_open_price: Optional[float] = Field(None,
                                            description="Returns trades where the open price is greater than or equal to this value.")
    max_open_price: Optional[float] = Field(None,
                                            description="Returns trades where the open price is less than or equal to this value.")
    min_close_price: Optional[float] = Field(None,
                                             description="Returns trades where the close price is greater than or equal to this value.")
    max_close_price: Optional[float] = Field(None,
                                             description="Returns trades where the close price is less than or equal to this value.")
    open_start: Optional[datetime] = Field(None,
                                           description="Returns trades opened after this date.")
    open_end: Optional[datetime] = Field(None,
                                         description="Returns trades opened before this date.")
    close_start: Optional[datetime] = Field(None,
                                            description="Returns trades closed after this date.")
    close_end: Optional[datetime] = Field(None,
                                          description="Returns trades closed before this date.")
    order_type: Optional[OrderType] = Field(None,
                                            description="Returns either LONG or SHORT orders.")


class Trade(Base):
    """
    Model representing a trade record.

    Attributes:
        order_id (UUID): Unique identifier for the trade.

        ticker (str): The ticker symbol for the trade (e.g., BTC-USDT).

        dollar_amount (float): The amount of money put onto the trade.

        realised_pnl (Optional[float]): The realised profit/loss upon position closure.
            This value will be None if the trade is still open.

        unrealised_pnl (Optional[float]): The current unrealised gain/loss for the trade.
            This value will indicate how much profit or loss the trade has generated but is not yet realized.

        open_price (float): The price at which the trade was opened.

        close_price (Optional[float]): The price at which the trade was closed.
            This will be None if the trade is still active.

        created_at (datetime): The timestamp when the trade was created.

        closed_at (Optional[datetime]): The timestamp when the trade was closed.
            This value will be None if the trade is still active.

        is_active (bool): Indicates whether the trade is currently active (True) or closed (False).

        order_type (Optional[OrderType]): The type of order, either LONG or SHORT.
            This indicates whether the trade is a buy (LONG) or sell (SHORT).
    """
    order_id: UUID = Field(description='Unique identifier for the trade')
    ticker: str
    dollar_amount: float = Field(description="The amount of money put onto the trade.")
    realised_pnl: Optional[float] = Field(None, description="The realised profit/loss upon position closure.")
    unrealised_pnl: Optional[float] = Field(None, description="The current unrealised gain/loss.")
    open_price: float = Field(description="The price at which the trade was opened.")
    close_price: Optional[float] = Field(None, description="The price at which the trade was closed.")
    created_at: datetime = Field(description="Timestamp when the trade was created.")
    closed_at: Optional[datetime] = Field(None, description="Timestamp when the trade was closed.")
    is_active: bool = Field(description="Indicates whether the trade is currently active.")
    order_type: Optional[OrderType] = Field(None, description="Indicates the order type: LONG or SHORT.")


class AssetAllocationRequestBody(Base):
    """
    False or True for the allocation of assets within an account
    """
    is_active: bool


class ProfitRequestBody(Base):
    close_start: Optional[datetime] = None
    close_end: Optional[datetime] = None


class GenerateKey(Base):
    """
    Model representing the generation of an API key.

    Attributes:
        api_key (str): The generated API key for accessing protected resources.
    """
    api_key: str = Field(description="The generated API key for accessing protected resources.")
