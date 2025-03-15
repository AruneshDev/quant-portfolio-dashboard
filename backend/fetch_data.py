import yfinance as yf
import pandas as pd
from sqlalchemy import create_engine

DATABASE_URL = "postgresql://admin:admin@data_storage:5432/portfolio_data"
engine = create_engine(DATABASE_URL)

def get_stock_data(ticker, start="2023-01-01", end="2024-01-01"):
    data = yf.download(ticker, start=start, end=end, auto_adjust=False)
    if not data.empty:
        data.to_sql(ticker.lower(), engine, if_exists='replace', index=False)
    return data

def get_live_price(ticker):
    try:
        stock = yf.Ticker(ticker).history(period="1d")
        return round(stock["Close"].iloc[-1], 2)
    except Exception as e:
        return {"error": f"Failed to fetch price for {ticker}: {str(e)}"}
