import streamlit as st
import pandas as pd
import requests
import plotly.graph_objects as go
import plotly.express as px

# 🎨 Set Page Config
st.set_page_config(page_title="📈 Quant Portfolio Dashboard", layout="wide")

# 📌 Backend URL
BACKEND_URL = "http://backend:8000"

# 📌 Sidebar
st.sidebar.image("assets/logo.png", width=100)
st.sidebar.title("📊 Portfolio Manager")
st.sidebar.write("Track, analyze, and optimize your investments in real-time.")

# 🔹 List of Tech Stocks
TECH_STOCKS = {
    "AAPL": "Apple", "MSFT": "Microsoft", "GOOGL": "Alphabet", "AMZN": "Amazon", "NVDA": "Nvidia",
    "META": "Meta Platforms", "TSLA": "Tesla", "ADBE": "Adobe", "CRM": "Salesforce", "AMD": "Advanced Micro Devices"
}

# 🔹 List of Available Time Periods
TIME_PERIODS = {
    "1D": "1d", "5D": "5d", "1M": "1mo", "6M": "6mo", "1Y": "1y", "MAX": "max"
}

# ✅ Ensure session state exists
if "portfolio" not in st.session_state:
    st.session_state.portfolio = {}

if "prices" not in st.session_state:
    st.session_state.prices = {}

# 🔹 User Portfolio Input
st.sidebar.subheader("📌 Add Your Stocks")
selected_ticker = st.sidebar.selectbox(
    "Select a Tech Stock:",
    list(TECH_STOCKS.keys()),
    format_func=lambda x: f"{x} ({TECH_STOCKS[x]})"
)
quantity = st.sidebar.number_input("Enter Quantity", min_value=1, step=1)

if st.sidebar.button("Add to Portfolio"):
    if selected_ticker in st.session_state.portfolio:
        st.session_state.portfolio[selected_ticker] += quantity
    else:
        st.session_state.portfolio[selected_ticker] = quantity
    st.rerun()  # Refresh UI on adding stock

# ✅ Function to Fetch Live Stock Prices from Backend
def fetch_prices():
    prices = {}
    for stock in st.session_state.portfolio.keys():
        response = requests.get(f"{BACKEND_URL}/price/{stock}")
        if response.status_code == 200:
            prices[stock] = response.json().get("price", 0.0)
        else:
            prices[stock] = 0.0
    return prices

# 🔹 Portfolio Summary Section
st.header("📊 Portfolio Overview")

if st.session_state.portfolio:
    portfolio_data = [
        {
            "Stock": stock,
            "Shares": shares,
            "Price": st.session_state.prices.get(stock, 0.0),
            "Total Value": shares * st.session_state.prices.get(stock, 0.0)
        }
        for stock, shares in st.session_state.portfolio.items()
    ]

    portfolio_df = pd.DataFrame(portfolio_data)

    # ✅ Fetch prices or use stored prices
    if not st.session_state.prices:
        st.session_state.prices = fetch_prices()

    portfolio_df["Price"] = portfolio_df["Stock"].map(st.session_state.prices)
    portfolio_df["Total Value"] = portfolio_df["Shares"] * portfolio_df["Price"]

    # 🚀 Show Total Portfolio Value on Top
    total_value = portfolio_df["Total Value"].sum()
    col1, col2 = st.columns([3, 1])
    col1.metric(label="💰 Total Portfolio Value", value=f"${total_value:,.2f}")

    # ✅ Refresh Button with Proper Function Call
    if col2.button("🔄 Refresh Prices", key="refresh_prices_button"):
        st.session_state.prices = fetch_prices()
        st.rerun()  # ✅ Refresh UI to reflect new prices

    # ✅ Store total portfolio value in session state for projections page
    st.session_state["portfolio_value"] = total_value

    # 📊 Portfolio Table
    st.dataframe(portfolio_df.style.format({"Price": "${:.2f}", "Total Value": "${:.2f}"}))

    # 📊 Portfolio Allocation Pie Chart
    fig = px.pie(portfolio_df, names="Stock", values="Total Value", title="Portfolio Allocation")
    st.plotly_chart(fig)

    # 📈 Stock Price Graph with Time Period Selection
    selected_graph_stock = st.selectbox("📊 Select a Stock to Visualize:", portfolio_df["Stock"])
    selected_period = st.selectbox("⏳ Select Time Period:", list(TIME_PERIODS.keys()))

    # ✅ Fetch historical stock data from Backend
    response = requests.get(f"{BACKEND_URL}/historical/{selected_graph_stock}?period={TIME_PERIODS[selected_period]}")

    if response.status_code == 200:
        stock_data = response.json().get("historical_data", [])

        if stock_data:
            df = pd.DataFrame(stock_data)
            df["date"] = pd.to_datetime(df["date"])
            df.set_index("date", inplace=True)

            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=df.index,
                y=df["close"],
                mode='lines',
                name=f'{selected_graph_stock} Price'
            ))

            fig.update_layout(
                title=f"📈 {selected_graph_stock} Price Trend - {selected_period}",
                xaxis_title='Date',
                yaxis_title='Price ($)',
                template="plotly_dark"
            )
            st.plotly_chart(fig)
        else:
            st.warning(f"❗ No historical data available for {selected_graph_stock}.")
    else:
        st.error(f"🚨 Error fetching historical data for {selected_graph_stock}. Try again later.")

else:
    st.warning("Add stocks to your portfolio to see data.")
