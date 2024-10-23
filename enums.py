from enum import Enum


class OrderType(str, Enum):
    LONG = 'long'
    SHORT = 'short'

