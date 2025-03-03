import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.express as px

# 🎨 Set Page Config
st.set_page_config(page_title="📈 Quant Portfolio Dashboard", layout="wide")

# 📌 Sidebar
st.sidebar.image("frontend/assets/logo.png", width=100)
st.sidebar.title("📊 Portfolio Manager")
st.sidebar.write("Track, analyze, and optimize your investments.")

# 🔹 List of Top 50 Tech Stocks (Ticker + Company Name)
TECH_STOCKS = {
    "AAPL": "Apple", "MSFT": "Microsoft", "GOOGL": "Alphabet", "AMZN": "Amazon", "NVDA": "Nvidia",
    "META": "Meta Platforms", "TSLA": "Tesla", "ADBE": "Adobe", "CRM": "Salesforce", "AMD": "Advanced Micro Devices",
    "INTC": "Intel", "CSCO": "Cisco", "IBM": "IBM Corporation", "ORCL": "Oracle", "PYPL": "PayPal",
    "NFLX": "Netflix", "UBER": "Uber Technologies", "SQ": "Block, Inc.", "SHOP": "Shopify", "TWLO": "Twilio",
    "SNOW": "Snowflake", "PLTR": "Palantir Technologies", "FSLY": "Fastly", "DOCU": "DocuSign", "ROKU": "Roku",
    "NET": "Cloudflare", "ZI": "ZoomInfo", "DDOG": "Datadog", "CRWD": "CrowdStrike", "ZS": "Zscaler",
    "MDB": "MongoDB", "OKTA": "Okta", "TEAM": "Atlassian", "ASAN": "Asana", "SMAR": "Smartsheet",
    "HUBS": "HubSpot", "SE": "Sea Limited", "BABA": "Alibaba", "JD": "JD.com", "PDD": "Pinduoduo",
    "TSM": "Taiwan Semiconductor", "AVGO": "Broadcom", "TXN": "Texas Instruments", "QCOM": "Qualcomm",
    "MU": "Micron Technology", "LRCX": "Lam Research", "NXPI": "NXP Semiconductors", "STX": "Seagate",
    "WDAY": "Workday", "SNAP": "Snap Inc."
}

# ✅ Ensure portfolio session state exists
if "portfolio" not in st.session_state:
    st.session_state.portfolio = {}

# 🔹 User Portfolio Input
st.sidebar.subheader("📌 Add Your Stocks")
selected_ticker = st.sidebar.selectbox("Select a Tech Stock:", list(TECH_STOCKS.keys()), format_func=lambda x: f"{x} ({TECH_STOCKS[x]})")
quantity = st.sidebar.number_input("Enter Quantity", min_value=1, step=1)

if st.sidebar.button("Add to Portfolio"):
    if selected_ticker in st.session_state.portfolio:
        st.session_state.portfolio[selected_ticker] += quantity  # ✅ Add to existing quantity
    else:
        st.session_state.portfolio[selected_ticker] = quantity  # ✅ Add new stock

# 🔹 Portfolio Summary Section
st.header("📊 Portfolio Overview")

if st.session_state.portfolio:
    portfolio_df = pd.DataFrame({"Stock": st.session_state.portfolio.keys(), "Shares": st.session_state.portfolio.values()})

    # Fetch live stock prices with error handling
    prices = {}
    for stock in portfolio_df["Stock"]:
        stock_data = yf.Ticker(stock).history(period="1d")
        prices[stock] = stock_data["Close"].iloc[-1] if not stock_data.empty else None

    portfolio_df["Price"] = portfolio_df["Stock"].map(prices)
    portfolio_df["Total Value"] = portfolio_df["Shares"] * portfolio_df["Price"]

    # 🚀 Show Total Portfolio Value on Top
    total_value = portfolio_df["Total Value"].sum(skipna=True)
    st.metric(label="💰 Total Portfolio Value", value=f"${total_value:,.2f}")

    # ✅ Store total portfolio value in session state for projections page
    st.session_state["portfolio_value"] = total_value

    # Display Portfolio Table
    st.dataframe(portfolio_df.style.format({"Price": "${:.2f}", "Total Value": "${:.2f}"}))

    # 📊 Portfolio Allocation Pie Chart
    fig = px.pie(portfolio_df, names="Stock", values="Total Value", title="Portfolio Allocation")
    st.plotly_chart(fig)

    # 🔹 Show Portfolio Value in Sidebar
    st.sidebar.write(f"💰 **Total Portfolio Value:** ${total_value:,.2f}")

    # 🚨 Show warning if any stock data is missing
    missing_stocks = [stock for stock, price in prices.items() if price is None]
    if missing_stocks:
        st.sidebar.warning(f"⚠️ No price data for: {', '.join(missing_stocks)}. Prices not available.")

else:
    st.warning("Add stocks to your portfolio to see data.")

# 🔹 Navigation to Projections Page
if st.button("📈 Go to Projections"):
    st.switch_page("pages/projections.py")
