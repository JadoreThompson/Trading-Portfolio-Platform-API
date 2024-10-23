import math
from typing import List


RISK_FREE = 4.0


def std(returns: List[float]) -> float:
    """Standard Deviation Calculation"""
    if not returns:
        return 0.0
    try:
        length_of_returns = len(returns)
        average_return = sum(returns) / length_of_returns
        individual_deviations = [(r - average_return) ** 2 for r in returns]
        return round(math.sqrt(sum(individual_deviations) / length_of_returns), 3)
    except ZeroDivisionError:
        return 0.0


def sharpe(returns: List[float], risk_free: float = None) -> float:
    """Sharpe Ratio"""
    risk_free = RISK_FREE if not risk_free else risk_free
    try:
        return (sum(returns) - (risk_free * len(returns))) / std(returns)
    except ZeroDivisionError:
        return 0.0


def downward_std(returns: List[float]) -> float:
    """Returns downside deviation"""
    try:
        length_of_returns = len(returns)
        average_return = sum(returns) / length_of_returns
        individual_deviations = [(r - average_return) ** 2 for r in returns]
        return round(math.sqrt(sum([d for d in individual_deviations if d < 0]) / length_of_returns), 3)
    except ZeroDivisionError:
        return 0.0


def sortino(returns: List[float], risk_free: float = None) -> float:
    """Returns the Sortino Ratio"""
    risk_free = RISK_FREE if not risk_free else risk_free
    try:
        return (sum(returns) / (risk_free * len(returns))) / downward_std(returns)
    except ZeroDivisionError:
        return 0.0


if __name__ == "__main__":
    result = sharpe([1])
    print(result)
