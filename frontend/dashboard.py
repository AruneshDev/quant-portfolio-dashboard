import streamlit as st
import requests
import json

# Set API base URL (localhost instead of 'backend')
API_BASE_URL = "http://backend:8000"

# Streamlit UI
st.set_page_config(page_title="📈 Quant Portfolio Dashboard", layout="wide")

st.title("📈 Quant Portfolio Dashboard")
st.write("Analyze your stock portfolio with live data, risk metrics, and optimization.")

# Sidebar Inputs for Portfolio
st.sidebar.header("Enter Portfolio")
portfolio_input = st.sidebar.text_area("Enter Portfolio (JSON format)", '{"AAPL": 0.4, "GOOGL": 0.3, "TSLA": 0.3}')
portfolio = json.loads(portfolio_input)

# Live Stock Price Checker
st.header("📊 Stock Price Checker")
ticker = st.text_input("Enter Stock Ticker (e.g., AAPL, TSLA, MSFT)", "AAPL")

if st.button("Get Live Price"):
    response = requests.get(f"{API_BASE_URL}/price/{ticker}")  # ✅ Corrected API URL
    if response.status_code == 200:
        data = response.json()
        st.success(f"Live Price of {ticker}: ${data['price']:.2f}")
    else:
        st.error("Error fetching stock price")

# Portfolio Analysis
st.header("📉 Portfolio Risk & Performance Metrics")
if st.button("Analyze Portfolio"):
    response = requests.post(f"{API_BASE_URL}/analyze", json=portfolio)
    if response.status_code == 200:
        st.json(response.json())
    else:
        st.error("Error analyzing portfolio")

# Portfolio Optimization
st.header("🔄 Portfolio Optimization")
if st.button("Optimize Portfolio"):
    response = requests.post(f"{API_BASE_URL}/optimize", json=portfolio)
    if response.status_code == 200:
        st.json(response.json())
    else:
        st.error("Error optimizing portfolio")
