from enum import Enum


class TradeStatusTypes(str, Enum):
    OPEN = 'open'
    CLOSED = 'closed'
    PARTIALLY_CLOSED = 'partially_closed'
