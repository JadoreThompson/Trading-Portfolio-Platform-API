from enum import Enum


class OrderType(str, Enum):
    LONG = 'long'
    SHORT = 'short'


class Intervals(str, Enum):
    MONTHLY = 'm'
    DAILY = 'd'
    YEARLY = 'y'


class Metrics(str, Enum):
    SHARPE = 'sharpe'
    SORTINO = 'sortino'
    STD = 'std'


class Ticker(str, Enum):
    SOL = 'SOL-USDT'
    BTC = 'BTC-USDT'
    ETH = 'ETH-USDT'
