import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.express as px

# 🎨 Set Page Config
st.set_page_config(page_title="📈 Quant Portfolio Dashboard", layout="wide")

# 📌 Sidebar
st.sidebar.image("frontend/assets/logo.png",width=100)
st.sidebar.title("📊 Portfolio Manager")
st.sidebar.write("Track, analyze, and optimize your investments.")

# 🔹 List of Top 50 Tech Stocks
TECH_STOCKS = [
    "AAPL", "MSFT", "GOOGL", "AMZN", "NVDA", "META", "TSLA", "ADBE", "CRM", "AMD",
    "INTC", "CSCO", "IBM", "ORCL", "PYPL", "NFLX", "UBER", "SQ", "SHOP", "TWLO",
    "SNOW", "PLTR", "FSLY", "DOCU", "ROKU", "NET", "ZI", "DDOG", "CRWD", "ZS",
    "MDB", "OKTA", "TEAM", "ASAN", "SMAR", "HUBS", "SE", "BABA", "JD", "PDD",
    "TSM", "AVGO", "TXN", "QCOM", "MU", "LRCX", "NXPI", "STX", "WDAY", "SNAP"
]

# ✅ Ensure portfolio session state exists
if "portfolio" not in st.session_state:
    st.session_state.portfolio = {}

# 🔹 User Portfolio Input
st.sidebar.subheader("📌 Add Your Stocks")
selected_stock = st.sidebar.selectbox("Select a Tech Stock:", TECH_STOCKS)
quantity = st.sidebar.number_input("Enter Quantity", min_value=1, step=1)

if st.sidebar.button("Add to Portfolio"):
    if selected_stock in st.session_state.portfolio:
        st.session_state.portfolio[selected_stock] += quantity  # ✅ Add to existing quantity
    else:
        st.session_state.portfolio[selected_stock] = quantity  # ✅ Add new stock

# 🔹 Portfolio Summary Section
st.header("📊 Portfolio Overview")

if st.session_state.portfolio:
    portfolio_df = pd.DataFrame({"Stock": st.session_state.portfolio.keys(), "Shares": st.session_state.portfolio.values()})
    
    # Fetch live stock prices
    prices = {stock: yf.Ticker(stock).history(period="1d")["Close"].iloc[-1] for stock in portfolio_df["Stock"]}
    portfolio_df["Price"] = portfolio_df["Stock"].map(prices)
    portfolio_df["Total Value"] = portfolio_df["Shares"] * portfolio_df["Price"]

    # 🚀 Show Total Portfolio Value on Top
    total_value = portfolio_df["Total Value"].sum()
    st.metric(label="💰 Total Portfolio Value", value=f"${total_value:,.2f}")

    # Display Portfolio Table
    st.dataframe(portfolio_df.style.format({"Price": "${:.2f}", "Total Value": "${:.2f}"}))

    # Portfolio Allocation Pie Chart
    fig = px.pie(portfolio_df, names="Stock", values="Total Value", title="Portfolio Allocation")
    st.plotly_chart(fig)
else:
    st.warning("Add stocks to your portfolio to see data.")

# 🔹 Navigation to Projections Page
if st.button("📈 Go to Projections"):
    st.switch_page("pages/projections.py")
