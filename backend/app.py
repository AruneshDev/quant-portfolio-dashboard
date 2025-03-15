from fastapi import FastAPI, Query
import yfinance as yf
from datetime import datetime, timedelta

app = FastAPI()

@app.get("/price/{ticker}")
def get_stock_price(ticker: str):
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period="1d")

        if hist.empty:
            return {"ticker": ticker, "price": None, "error": "No data available"}

        price = hist["Close"].iloc[-1] if not hist["Close"].isna().all() else None
        return {"ticker": ticker, "price": price}

    except Exception as e:
        return {"error": f"Failed to fetch price for {ticker}: {str(e)}"}

@app.get("/historical/{ticker}")
async def get_historical_data(ticker: str, period: str = Query("1mo", description="Time period (1d, 5d, 1mo, 6mo, 1y, max)")):
    try:
        stock = yf.Ticker(ticker)
        stock_data = stock.history(period=period)

        if stock_data.empty:
            return {"error": f"No historical data found for {ticker} for period {period}"}

        historical_prices = [
            {"date": str(index.date()), "close": row["Close"]}
            for index, row in stock_data.iterrows()
        ]

        return {"historical_data": historical_prices}

    except Exception as e:
        return {"error": f"Failed to fetch historical data for {ticker}: {str(e)}"}
