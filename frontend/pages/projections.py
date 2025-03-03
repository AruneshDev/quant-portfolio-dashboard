import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="📈 Portfolio Projections", layout="wide")
st.title("📈 Portfolio Projections")
st.write("Estimate your future portfolio value using Monte Carlo simulations.")

# 🚀 User Inputs
num_simulations = st.slider("Number of Simulations", min_value=100, max_value=5000, value=1000)
years = st.slider("Investment Horizon (Years)", min_value=1, max_value=10, value=5)

# ✅ Ensure portfolio session state exists
if "portfolio_value" not in st.session_state:
    st.session_state.portfolio_value = 100000  # Default starting value

initial_value = st.session_state.portfolio_value
expected_return = 0.07  # 7% average annual return
volatility = 0.15  # 15% standard deviation

# 🚀 Monte Carlo Simulation
simulations = []
for _ in range(num_simulations):
    future_value = [initial_value]
    for _ in range(years * 252):  # 252 trading days per year
        daily_return = np.random.normal(expected_return / 252, volatility / np.sqrt(252))
        future_value.append(future_value[-1] * (1 + daily_return))
    simulations.append(future_value)

# 🔹 Plot Projections
fig, ax = plt.subplots(figsize=(10, 4))
ax.plot(np.array(simulations).T, alpha=0.1, color="blue")
ax.set_title(f"Monte Carlo Simulations ({num_simulations} runs)")
st.pyplot(fig)

# 🚀 Estimated Portfolio Value Range
final_values = [sim[-1] for sim in simulations]
st.write(f"📌 **Projected Portfolio Value (5-Year Estimate)**:")
st.metric(label="🔹 Average Projection", value=f"${np.mean(final_values):,.2f}")
st.metric(label="🔹 95% Confidence Interval", value=f"${np.percentile(final_values, 5):,.2f} - ${np.percentile(final_values, 95):,.2f}")

st.markdown("---")
if st.button("⬅ Go Back"):
    st.switch_page("dashboard.py")
