import yfinance as yf
import pandas as pd

def get_stock_data(ticker, start="2023-01-01", end="2024-01-01"):
    """
    Fetch historical stock data for a given ticker.
    """
    stock = yf.Ticker(ticker)
    data = stock.history(start=start, end=end)
    return data

def get_live_price(ticker):
    """
    Fetch the latest stock price.
    """
    stock = yf.Ticker(ticker)
    try:
        price = stock.history(period="1d")["Close"].iloc[-1]
        return round(price, 2)
    except Exception as e:
        return {"error": f"Failed to fetch price for {ticker}: {str(e)}"}

if __name__ == "__main__":
    # Test fetching historical data
    ticker = "AAPL"
    print("Fetching historical data for:", ticker)
    df = get_stock_data(ticker)
    print(df.head())

    # Test fetching live price
    print("\nFetching live price for:", ticker)
    print(get_live_price(ticker))
