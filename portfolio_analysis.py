import numpy as np
import pandas as pd
from scipy.stats import norm
from fetch_data import get_stock_data
from pypfopt.efficient_frontier import EfficientFrontier
from pypfopt.risk_models import CovarianceShrinkage
from pypfopt.expected_returns import mean_historical_return

def calculate_portfolio_returns(portfolio):
    """
    Calculate daily portfolio returns.
    :param portfolio: Dictionary of {ticker: weight}
    :return: Portfolio returns dataframe
    """
    df = pd.DataFrame()
    for stock, weight in portfolio.items():
        df[stock] = get_stock_data(stock)["Close"].pct_change()

    df.dropna(inplace=True)
    portfolio_returns = df.dot(np.array(list(portfolio.values())))
    return portfolio_returns

def calculate_sharpe_ratio(portfolio_returns, risk_free_rate=0.02):
    """
    Compute the Sharpe Ratio for a portfolio.
    """
    excess_return = portfolio_returns.mean() - risk_free_rate / 252
    return np.sqrt(252) * excess_return / portfolio_returns.std()

def calculate_var(portfolio_returns, confidence_level=0.95):
    """
    Calculate Value at Risk (VaR) using historical method.
    """
    mean = portfolio_returns.mean()
    std_dev = portfolio_returns.std()
    return norm.ppf(1 - confidence_level, mean, std_dev)

def analyze_portfolio(portfolio):
    """
    Perform portfolio analysis by calculating key risk metrics.
    :param portfolio: Dictionary of {ticker: weight}
    :return: Dictionary with Sharpe Ratio, VaR, and Portfolio Volatility
    """
    portfolio_returns = calculate_portfolio_returns(portfolio)
    sharpe = calculate_sharpe_ratio(portfolio_returns)
    var = calculate_var(portfolio_returns)
    volatility = portfolio_returns.std() * np.sqrt(252)

    return {
        "Sharpe Ratio": round(sharpe, 3),
        "Value at Risk (VaR)": round(var, 3),
        "Portfolio Volatility": round(volatility, 3)
    }

def optimize_portfolio(portfolio):
    """
    Use Modern Portfolio Theory to find the optimal asset allocation.
    """
    df = pd.DataFrame()
    for stock in portfolio.keys():
        df[stock] = get_stock_data(stock)["Close"]

    returns = df.pct_change().dropna()
    mu = mean_historical_return(df)
    S = CovarianceShrinkage(df).ledoit_wolf()

    ef = EfficientFrontier(mu, S)
    weights = ef.max_sharpe()
    return ef.clean_weights()

if __name__ == "__main__":
    # Example portfolio
    portfolio = {"AAPL": 0.4, "GOOGL": 0.3, "TSLA": 0.3}
    
    print("\n📊 Portfolio Analysis:")
    print(analyze_portfolio(portfolio))

    print("\n🔄 Optimized Portfolio Allocation:")
    print(optimize_portfolio(portfolio))
