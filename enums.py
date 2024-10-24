from enum import Enum


class OrderType(str, Enum):
    LONG = 'long'
    SHORT = 'short'


class Metrics(str, Enum):
    SHARPE = 'sharpe'
    SORTINO = 'sortino'


class Ticker(str, Enum):
    SOL = 'SOL-USDT'
    BTC = 'BTC-USDT'
    ETH = 'ETH-USDT'
