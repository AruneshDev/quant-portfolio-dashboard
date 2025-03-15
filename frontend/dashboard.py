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

# 🔹 List of Top 10 Tech Stocks
TECH_STOCKS = {
    "AAPL": "Apple", "MSFT": "Microsoft", "GOOGL": "Alphabet", "AMZN": "Amazon", "NVDA": "Nvidia",
    "META": "Meta Platforms", "TSLA": "Tesla", "ADBE": "Adobe", "CRM": "Salesforce", "AMD": "Advanced Micro Devices"
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
    st.session_state.portfolio[selected_ticker] = st.session_state.portfolio.get(selected_ticker, 0) + quantity
    st.rerun()  # Refresh UI on adding stock

# ✅ Function to Fetch Live Stock Prices from Backend
def fetch_prices():
    prices = {}
    for stock in st.session_state.portfolio.keys():
        response = requests.get(f"{BACKEND_URL}/price/{stock}")
        if response.status_code == 200 and "price" in response.json():
            prices[stock] = response.json().get("price", 0.0)
        else:
            prices[stock] = 0.0  # Handle errors gracefully
    return prices

# 🔹 Portfolio Summary Section
st.header("📊 Portfolio Overview")

if st.session_state.portfolio:
    # ✅ Fetch prices if not already stored
    if not st.session_state.prices:
        st.session_state.prices = fetch_prices()

    # ✅ Create Portfolio DataFrame
    portfolio_df = pd.DataFrame([
        {
            "Stock": stock,
            "Shares": shares,
            "Price": st.session_state.prices.get(stock, 0.0),
            "Total Value": shares * st.session_state.prices.get(stock, 0.0)
        }
        for stock, shares in st.session_state.portfolio.items()
    ])

    # 🚀 Display Total Portfolio Value
    total_value = portfolio_df["Total Value"].sum()
    col1, col2 = st.columns([3, 1])
    col1.metric(label="💰 Total Portfolio Value", value=f"${total_value:,.2f}")

    # ✅ Refresh Button with Proper Function Call
    if col2.button("🔄 Refresh Prices", key="refresh_prices_button"):
        st.session_state.prices = fetch_prices()
        st.rerun()

    # ✅ Store portfolio value for projections
    st.session_state["portfolio_value"] = total_value

    # 📊 Portfolio Table
    st.dataframe(portfolio_df.style.format({"Price": "${:.2f}", "Total Value": "${:.2f}"}))

    # 📊 Portfolio Allocation Pie Chart
    fig = px.pie(portfolio_df, names="Stock", values="Total Value", title="Portfolio Allocation")
    st.plotly_chart(fig)

    # 📈 Stock Price Graph
    selected_graph_stock = st.selectbox("📊 Select a Stock to Visualize:", portfolio_df["Stock"])

    # ✅ Fetch historical stock data from Backend
    response = requests.get(f"{BACKEND_URL}/historical/{selected_graph_stock}")

    if response.status_code == 200 and "historical_data" in response.json():
        stock_data = response.json()["historical_data"]

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
                title=f"📈 {selected_graph_stock} Price Trend",
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
    st.warning("📌 Add stocks to your portfolio to see data.")
