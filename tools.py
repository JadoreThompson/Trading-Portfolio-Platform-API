import math
from typing import List, Tuple


# Arithmetic Tools
def sharpe_std(returns: List[int | float]) -> float | str:
    """
    Calculates the standard deviation for the returns in the dataset.
    Takes both positive and negative data points into account (as per Sharpe ratio method).
    """
    try:
        mean = sum(returns) / len(returns)
        deviations = [float(num) - mean for num in returns]
        deviations_square = [num ** 2 for num in deviations]
        average_deviation = sum(deviations_square) / len(deviations_square)
        return float(math.sqrt(average_deviation))
    except ZeroDivisionError:
        raise ZeroDivisionError("Can't divide by 0")
    except TypeError:
        raise TypeError("Must all be valid numbers, no words allowed")


def sharpe_ratio(portfolio_return, periodic_returns, risk_free_return=4.0) -> int | float:
    """
    Calculates the Sharpe ratio, which measures the excess return per unit of risk.
    Fixed bond rate of 4.0 is used as the risk-free return.
    """

    return (portfolio_return - (risk_free_return * len(periodic_returns))) / sharpe_std(periodic_returns)


def sortino_std(periodic_returns, risk_free_return) -> int | float:
    """
    Calculates the Sortino standard deviation, considering only negative deviations (downside risk).
    Fixed bond rate of 4.0 is used as the risk-free return.
    """
    try:
        avg_risk_free_return = risk_free_return / len(periodic_returns)
        negative_deviations = [(num - avg_risk_free_return) for num in periodic_returns if (num - avg_risk_free_return) < 0]
        squared_negatives = [num ** 2 for num in negative_deviations]
        return math.sqrt(sum(squared_negatives) / len(squared_negatives))
    except ZeroDivisionError:
        raise ZeroDivisionError("Can't divide by 0")
    except TypeError:
        raise TypeError("Can't have non-numeric characters")


def sortino_ratio(portfolio_return, periodic_returns, risk_free_return=4.0) -> int | float:
    """
    Calculates the Sortino Ratio, which measures the risk-adjusted return considering only downside risk.
    Fixed bond rate of 4.0 is used as the risk-free return.
    """
    return (portfolio_return - (risk_free_return * len(periodic_returns))) / sortino_std(periodic_returns, risk_free_return)


def beta(portfolio_periodic_return, benchmark_return, benchmark_periodic_return=None) -> int | float:
    """
    Calculates the Beta of a portfolio relative to a benchmark.
    Beta is a measure of the portfolio's sensitivity to market movements.
    """
    try:
        portfolio_avg = sum(portfolio_periodic_return) / len(portfolio_periodic_return)
        benchmark_avg = benchmark_return / len(portfolio_periodic_return)

        portfolio_variances = [(item - portfolio_avg) for item in portfolio_periodic_return]

        if benchmark_periodic_return is None:
            benchmark_periodic_return = [benchmark_return] * len(portfolio_periodic_return)

        benchmark_variances = [(item - benchmark_avg) for item in benchmark_periodic_return]

        if len(portfolio_variances) != len(benchmark_variances):
            raise ValueError("The lengths of portfolio and benchmark variances must be the same.")

        period = len(portfolio_variances)
        covariance_list = []
        for i in range(0, len(portfolio_variances)):
            covariance_list.append(portfolio_variances[i] * benchmark_variances[i])

        variance_list = [item ** 2 for item in benchmark_variances]

        covariance = sum(covariance_list) / period
        variance = sum(variance_list) / period

        return covariance / variance
    except ZeroDivisionError:
        raise ZeroDivisionError


def treynor_ratio(portfolio_return, periodic_returns, risk_free_return=4.0) -> int | float:
    """
    Calculates the Treynor Ratio, which measures the portfolio's return per unit of risk (beta).
    Fixed bond rate of 4.0 is used as the risk-free return.
    """
    try:
        return (portfolio_return - (len(periodic_returns) * risk_free_return)) / beta(periodic_returns, risk_free_return)
    except ZeroDivisionError:
        return 0


# Database Tool
def generate_select_args(params: dict) -> Tuple[str, str, str, list]:
    """
    :param params:(dict):
    :return: Tuple
    - string of columns e.g. name, sname, color
    - string of placeholders e.g. $1, $2, $3
    - list of values e.g. jeff, thompson, red
    """
    try:
        cols = [key for key, value in params.items() if value]
        placeholders = [f"${i}" for i in range(1, len(cols) + 1)]

        query_conditions = []
        i = 0
        if params['trade_open_time']:
            query_conditions.append(f"trade_open_time >= {i}")
            i += 1
        if params['trade_close_time']:
            query_conditions.append(f"trade_close_time <= {i}")
            i += 1
        if params['symbol']:
            query_conditions.append(f"symbol = {i}")
            i += 1

        args = [params[key] for key in cols]
        return ", ".join(cols), ", ".join(placeholders), " AND ".join(query_conditions), args
    except Exception as e:
        raise Exception(e)


def test():
    pass


if __name__ == "__main__":
    test()
