import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.express as px

# 🎨 **Page Configuration**
st.set_page_config(page_title="📈 Quant Portfolio Dashboard", layout="wide")

# 📌 **Sidebar Logo & Title**
st.sidebar.image("frontend/assets/logo.png", width=100)
st.sidebar.title("📊 Portfolio Manager")
st.sidebar.write("Track, analyze, and optimize your investments.")

# 🔹 **List of Top 50 Tech Stocks (Ticker + Company Name)**
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

# ✅ **Ensure Session State for Portfolio**
if "portfolio" not in st.session_state:
    st.session_state.portfolio = {}

if "prices" not in st.session_state:
    st.session_state.prices = {}

# 🔹 **User Portfolio Input (Stock Selection & Quantity)**
st.sidebar.subheader("📌 Add Your Stocks")
selected_ticker = st.sidebar.selectbox(
    "Select a Tech Stock:", list(TECH_STOCKS.keys()), format_func=lambda x: f"{x} ({TECH_STOCKS[x]})"
)
quantity = st.sidebar.number_input("Enter Quantity", min_value=1, step=1)

if st.sidebar.button("➕ Add to Portfolio"):
    if selected_ticker in st.session_state.portfolio:
        st.session_state.portfolio[selected_ticker] += quantity
    else:
        st.session_state.portfolio[selected_ticker] = quantity
    st.rerun()  # ✅ Instantly updates the UI with new stock

# ✅ **Function to Fetch Live Stock Prices**
def fetch_prices():
    prices = {}
    for stock in st.session_state.portfolio.keys():
        stock_data = yf.Ticker(stock).history(period="1d")
        prices[stock] = stock_data["Close"].iloc[-1] if not stock_data.empty else None
    return prices

# 🔹 **Portfolio Summary Section**
st.header("📊 Portfolio Overview")

if st.session_state.portfolio:
    portfolio_df = pd.DataFrame({"Stock": st.session_state.portfolio.keys(), "Shares": st.session_state.portfolio.values()})

    # ✅ Fetch or Use Stored Prices
    if not st.session_state.prices:
        st.session_state.prices = fetch_prices()

    portfolio_df["Price"] = portfolio_df["Stock"].map(st.session_state.prices)
    portfolio_df["Total Value"] = portfolio_df["Shares"] * portfolio_df["Price"]

    # 🚀 **Show Total Portfolio Value on Top**
    total_value = portfolio_df["Total Value"].sum(skipna=True)

    col1, col2 = st.columns([3, 1])
    col1.metric(label="💰 Total Portfolio Value", value=f"${total_value:,.2f}")

    # ✅ **Refresh Button with Proper Function Call**
    if col2.button("🔄 Refresh Prices", key="refresh_prices_button"):
        st.session_state.prices = fetch_prices()
        st.rerun()  # ✅ UI instantly refreshes with new prices

    # ✅ **Store Portfolio Value for Projections Page**
    st.session_state["portfolio_value"] = total_value

    # 📊 **Display Portfolio Table**
    st.dataframe(portfolio_df.style.format({"Price": "${:.2f}", "Total Value": "${:.2f}"}))

    # 📊 **Portfolio Allocation Pie Chart**
    fig = px.pie(portfolio_df, names="Stock", values="Total Value", title="Portfolio Allocation")
    st.plotly_chart(fig)

    # 🔹 **Show Portfolio Value in Sidebar**
    st.sidebar.write(f"💰 **Total Portfolio Value:** ${total_value:,.2f}")

    # 🚨 **Warning for Missing Prices**
    missing_stocks = [stock for stock, price in st.session_state.prices.items() if price is None]
    if missing_stocks:
        st.sidebar.warning(f"⚠️ No price data for: {', '.join(missing_stocks)}.")

else:
    st.warning("📌 Add stocks to your portfolio to see data.")

# 🔹 **Navigation to Projections Page**
if st.button("📈 Go to Projections"):
    st.switch_page("pages/projections.py")
