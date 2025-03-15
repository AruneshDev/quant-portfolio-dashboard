from fastapi import FastAPI
import yfinance as yf
from datetime import datetime, timedelta
import pandas as pd

app = FastAPI()

# ✅ Route to Fetch Current Stock Price
@app.get("/price/{ticker}")
def get_stock_price(ticker: str):
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period="1d")

        # ✅ Handle cases where data might be missing
        if hist.empty or hist["Close"].isna().all():
            return {"ticker": ticker, "price": 0.0, "error": "No data available"}

        price = hist["Close"].iloc[-1] if not hist["Close"].isna().all() else 0.0
        return {"ticker": ticker, "price": round(price, 2)}  # Return price rounded to 2 decimal places

    except Exception as e:
        return {"error": f"Failed to fetch price for {ticker}: {str(e)}"}

# ✅ Route to Fetch Historical Data for the Last 30 Days
@app.get("/historical/{ticker}")
async def get_historical_data(ticker: str):
    try:
        stock = yf.Ticker(ticker)
        stock_data = stock.history(period="1mo")

        # ✅ Handle cases where historical data is missing
        if stock_data.empty:
            return {"error": f"No historical data found for {ticker}"}

        # ✅ Ensure valid data by filtering out missing values
        historical_prices = [
            {"date": str(index.date()), "close": round(row["Close"], 2)}
            for index, row in stock_data.iterrows()
            if not pd.isna(row["Close"])
        ]

        return {"ticker": ticker, "historical_data": historical_prices}

    except Exception as e:
        return {"error": f"Failed to fetch historical data for {ticker}: {str(e)}"}

# ✅ Health Check Route
@app.get("/")
def health_check():
    return {"status": "API is running!"}
