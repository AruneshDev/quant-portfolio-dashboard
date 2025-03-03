import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
import yfinance as yf

st.title("📈 Monte Carlo Portfolio Projections")

# ✅ Get Portfolio from Session State
if "portfolio" not in st.session_state or not st.session_state.portfolio:
    st.error("⚠️ No portfolio found! Please add stocks in the dashboard.")
    st.stop()

portfolio_tickers = list(st.session_state.portfolio.keys())
weights = np.array([shares for shares in st.session_state.portfolio.values()])

# ✅ Normalize Weights
weights = weights / np.sum(weights)

# ✅ Fetch Stock Data
def get_historical_returns(tickers, period="5y"):
    try:
        data = yf.download(tickers, period=period)
        
        # ✅ Check if 'Adj Close' exists, else use 'Close'
        if "Adj Close" in data.columns:
            prices = data["Adj Close"]
        elif "Close" in data.columns:
            prices = data["Close"]
        else:
            st.error("⚠️ No valid price data found. Check the tickers.")
            return None

        returns = prices.pct_change().dropna()  # ✅ Daily Returns
        return returns

    except Exception as e:
        st.error(f"⚠️ Error fetching stock data: {str(e)}")
        return None

returns = get_historical_returns(portfolio_tickers)

if returns is None:
    st.stop()  # 🚨 Stop execution if no valid data

# ✅ Compute Portfolio Return
portfolio_return = returns.dot(weights)

# 🎯 **User Inputs for Simulation**
num_simulations = st.sidebar.slider("🔢 Number of Simulations", 100, 5000, 1000, step=100)
years = st.sidebar.slider("📅 Time Horizon (Years)", 1.0, 10.0, 5.0, step=0.5)
time_horizon = int(years * 252)

initial_portfolio_value = st.sidebar.number_input(
    "💰 Initial Portfolio Value ($)",
    value=float(st.session_state.get("portfolio_value", 100000.0)), 
    step=5000.0
)

# ✅ Monte Carlo Simulation
np.random.seed(42)
simulations = np.zeros((num_simulations, time_horizon))
simulations[:, 0] = initial_portfolio_value

for i in range(1, time_horizon):
    daily_return = np.random.choice(portfolio_return, size=num_simulations)  # Sample historical returns
    simulations[:, i] = simulations[:, i-1] * (1 + daily_return)

# 📊 Compute Statistics
avg_projection = simulations.mean(axis=0)
min_projection = np.percentile(simulations, 5, axis=0)
max_projection = np.percentile(simulations, 95, axis=0)

# 🎨 Plot Monte Carlo Projections
fig, ax = plt.subplots(figsize=(10, 5))
ax.fill_between(range(time_horizon), min_projection, max_projection, color='blue', alpha=0.15, label="90% Confidence Interval")
ax.plot(avg_projection, color='red', linewidth=2, label="Projected Growth")

ax.set_title("Monte Carlo Portfolio Simulations", fontsize=14)
ax.set_xlabel("Trading Days", fontsize=12)
ax.set_ylabel("Portfolio Value ($)", fontsize=12)
ax.legend()
ax.grid(True, linestyle='--', alpha=0.5)

st.pyplot(fig)

# 📌 Summary Stats
st.markdown("### 📌 Projected Portfolio Value (End of Simulation):")
st.markdown(f"**📊 Average Projection:**\n# ${avg_projection[-1]:,.2f}")
st.markdown(f"**📉 5th Percentile (Worst-Case):**\n# ${min_projection[-1]:,.2f}")
st.markdown(f"**📈 95th Percentile (Best-Case):**\n# ${max_projection[-1]:,.2f}")
