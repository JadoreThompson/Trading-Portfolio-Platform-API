import math
from typing import List


def sharpe_std(returns) -> float | str:
    """
     - Calculates the standard deviation for the returns in the dataset.
     - Takes both positive and negative data points into account (as per Sharpe ratio method).
    :param returns: (List[int or float]) A list of returns over a period.
    :return: (float or str) Standard deviation of returns. If error, returns a descriptive string.
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


def sharpe_ratio(portfolio_return, periodic_returns, risk_free_rate):
    """
    Calculates the Sharpe ratio, which measures the excess return per unit of risk.
    Sharpe ratio formula: (Portfolio Return - Risk-Free Return) / Standard Deviation of Portfolio Returns.

    :param portfolio_return: (float) Total return of the portfolio across the entire period.
    :param periodic_returns: (List[int or float]) A list of periodic returns of the portfolio.
    :param risk_free_rate: (float) The return of a risk-free asset over the same period.
    :return: (float) The Sharpe Ratio.
        - Sharpe ratio < 1: Inefficient returns per unit of risk.
        - Sharpe ratio >= 1: Reasonable return per unit of risk.
        - Sharpe ratio >= 2: Favorable return per unit of risk.
    """
    return (portfolio_return - risk_free_rate) / sharpe_std(periodic_returns)


def sortino_std(periodic_returns, risk_free_return) -> int | float:
    """
    Calculates the Sortino standard deviation, which only considers negative deviations (downside risk).

    :param periodic_returns: (List[int or float]) A list of periodic returns of the portfolio.
    :param risk_free_return: (float) The return of a risk-free asset over the same period.
    :return: (float or str) Standard deviation of negative returns. If error, returns a descriptive string.
    """
    try:
        avg_risk_free_return = risk_free_return / len(periodic_returns)
        negative_deviations = [(num - avg_risk_free_return) for num in periodic_returns if
                               (num - avg_risk_free_return) < 0]

        squared_negatives = [num ** 2 for num in negative_deviations]
        return math.sqrt(sum(squared_negatives) / len(squared_negatives))
    except ZeroDivisionError:
        raise ZeroDivisionError("Can't divide by 0")
    except TypeError:
        raise TypeError("Can't have non numeric characters")


def sortino_ratio(portfolio_return, periodic_returns, risk_free_return):
    """
    Calculates the Sortino Ratio, which measures the risk-adjusted return considering only downside risk.
    Sortino Ratio formula: (Portfolio Return - Risk-Free Return) / Downside Deviation.

    :param portfolio_return: (float) Total return of the portfolio across the entire period.
    :param periodic_returns: (List[int or float]) A list of periodic returns of the portfolio.
    :param risk_free_return: (float) The return of a risk-free asset over the same period.
    :return: (float) The Sortino Ratio.
    """
    return (portfolio_return - risk_free_return) / sortino_std(periodic_returns, risk_free_return)


def beta(portfolio_periodic_return, benchmark_return, benchmark_periodic_return=None) -> int | float:
    """
    Calculates the Beta of a portfolio relative to a benchmark. Beta is a measure of the portfolio's sensitivity to market movements.

    Formula: Beta = Covariance(Portfolio Returns, Benchmark Returns) / Variance(Benchmark Returns).

    :param portfolio_periodic_return: (List[int or float]) A list of periodic returns of the portfolio.
    :param benchmark_return: (float) The average return of the benchmark asset (e.g., market index).
    :param benchmark_periodic_return: (List[int or float], optional) A list of periodic returns of the benchmark asset.
        If not provided, the benchmark return is used across the entire period.
    :return: (float) The Beta of the portfolio.
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


def treynor_ratio(portfolio_return, periodic_returns, risk_free_return):
    """
    Calculates the Treynor Ratio, which measures the portfolio's return per unit of risk (beta).
    Treynor Ratio formula: (Portfolio Return - Risk-Free Return) / Beta.

    :param portfolio_return: (float) Total return of the portfolio across the entire period.
    :param periodic_returns: (List[int or float]) A list of periodic returns of the portfolio.
    :param risk_free_return: (float) The return of a risk-free asset over the same period.
    :return: (float) The Treynor Ratio.
    """
    try:
        return (portfolio_return - risk_free_return) / beta(periodic_returns, risk_free_return)
    except ZeroDivisionError:
        return 0


def test():
    """
    A test function to calculate and print the Sharpe, Sortino, and Treynor ratios for a sample portfolio.
    """
    portfolio_return = 7
    periodic_returns = [-1, 6, 8, 9]
    risk_free_return = 4.25

    print("Performance Across {} months".format(len(periodic_returns)))
    print("- Sharpe Ratio: {}".format(sharpe_ratio(portfolio_return, periodic_returns, risk_free_return)))
    print("- Sortino Ratio: {}".format(sortino_ratio(portfolio_return, periodic_returns, risk_free_return)))
    print("- Treynor Ratio: {}".format(treynor_ratio(portfolio_return, periodic_returns, risk_free_return)))


if __name__ == "__main__":
    test()
