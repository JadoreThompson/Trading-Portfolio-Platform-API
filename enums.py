from enum import Enum


class TradeStateTypes(str, Enum):
    OPEN = 'OPEN'
    CLOSED = 'CLOSED'
    CLOSE_WHEN_TRADEABLE = 'CLOSE_WHEN_TRADEABLE'
    ALL = 'ALL'