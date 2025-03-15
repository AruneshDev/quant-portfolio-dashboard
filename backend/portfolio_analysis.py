import numpy as np
import pandas as pd
from scipy.stats import norm
from fetch_data import get_stock_data
from pypfopt.efficient_frontier import EfficientFrontier
from pypfopt.risk_models import CovarianceShrinkage
from pypfopt.expected_returns import mean_historical_return

def calculate_portfolio_returns(portfolio):
    df = pd.DataFrame()
    for stock, weight in portfolio.items():
        df[stock] = get_stock_data(stock)["Close"].pct_change()

    df.dropna(inplace=True)
    portfolio_returns = df.dot(np.array(list(portfolio.values())))
    return portfolio_returns

def calculate_sharpe_ratio(portfolio_returns, risk_free_rate=0.02):
    excess_return = portfolio_returns.mean() - risk_free_rate / 252
    return np.sqrt(252) * excess_return / portfolio_returns.std()

def analyze_portfolio(portfolio):
    portfolio_returns = calculate_portfolio_returns(portfolio)
    sharpe = calculate_sharpe_ratio(portfolio_returns)
    volatility = portfolio_returns.std() * np.sqrt(252)

    return {
        "Sharpe Ratio": round(sharpe, 3),
        "Portfolio Volatility": round(volatility, 3)
    }

def optimize_portfolio(portfolio):
    df = pd.DataFrame()
    for stock in portfolio.keys():
        df[stock] = get_stock_data(stock)["Close"]

    returns = df.pct_change().dropna()
    mu = mean_historical_return(df)
    S = CovarianceShrinkage(df).ledoit_wolf()

    ef = EfficientFrontier(mu, S)
    weights = ef.max_sharpe()
    return ef.clean_weights()
