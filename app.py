from fastapi import FastAPI
from fetch_data import get_live_price
from portfolio_analysis import analyze_portfolio, optimize_portfolio

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Welcome to the Quant Portfolio API!"}

@app.get("/health")
def health():
    return {"status": "running"}

@app.get("/price/{ticker}")
def price(ticker: str):
    return {"ticker": ticker, "price": get_live_price(ticker)}

@app.post("/analyze")
def analyze(portfolio: dict):
    return analyze_portfolio(portfolio)

@app.post("/optimize")
def optimize(portfolio: dict):
    return optimize_portfolio(portfolio)
