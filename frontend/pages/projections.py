import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

# 🎯 **Streamlit UI - User Inputs**
st.title("📈 Monte Carlo Portfolio Projections")

# Sliders for user-defined parameters
num_simulations = st.sidebar.slider("🔢 Number of Simulations", 100, 5000, 1000, step=100)

# Convert years to trading days (1 year = 252 trading days)
years = st.sidebar.slider("📅 Time Horizon (Years)", 1.0, 10.0, 5.0, step=0.5)  # 1 to 10 years
time_horizon = int(years * 252)  # Convert selected years to days

# Get initial portfolio value from session state (default: 100000)
initial_portfolio_value = st.sidebar.number_input(
    "💰 Initial Portfolio Value ($)",
    value=float(st.session_state.get("portfolio_value", 100000.0)),  # Ensure float value
    step=5000.0  # Ensure float step to avoid errors
)

# User-defined market assumptions
expected_annual_return = st.sidebar.slider("📈 Expected Annual Return (%)", -10.0, 30.0, 8.0, step=0.5) / 100
annual_volatility = st.sidebar.slider("📊 Annual Volatility (%)", 5.0, 50.0, 20.0, step=0.5) / 100

# Convert to daily return values
mean_return = expected_annual_return / 252  # Convert annual return to daily return
volatility = annual_volatility / np.sqrt(252)  # Convert annual volatility to daily volatility

# 🧠 **Simulating Monte Carlo projections**
np.random.seed(42)
simulations = np.zeros((num_simulations, time_horizon))
simulations[:, 0] = initial_portfolio_value

for i in range(1, time_horizon):
    simulations[:, i] = simulations[:, i-1] * (1 + np.random.normal(mean_return, volatility, num_simulations))

# 📊 **Compute Statistics**
avg_projection = simulations.mean(axis=0)
min_projection = np.percentile(simulations, 5, axis=0)  # 5th percentile (worst-case)
max_projection = np.percentile(simulations, 95, axis=0)  # 95th percentile (best-case)

# 🎨 **Plot the Monte Carlo Projections**
fig, ax = plt.subplots(figsize=(10, 5))

# Plot min-max range as a shaded area
ax.fill_between(range(time_horizon), min_projection, max_projection, color='blue', alpha=0.15, label="90% Confidence Interval")

# Plot the main trend line (average projection)
ax.plot(avg_projection, color='red', linewidth=2, label="Projected Growth")

# Formatting the graph
ax.set_title("Monte Carlo Portfolio Simulations", fontsize=14)
ax.set_xlabel("Trading Days", fontsize=12)
ax.set_ylabel("Portfolio Value ($)", fontsize=12)
ax.legend()
ax.grid(True, linestyle='--', alpha=0.5)

# Display the plot
st.pyplot(fig)

# 📌 **Display Summary Statistics**
st.markdown("### 📌 Projected Portfolio Value (End of Simulation):")
st.markdown(f"**📊 Average Projection:**\n# ${avg_projection[-1]:,.2f}")
st.markdown(f"**📉 5th Percentile (Worst-Case):**\n# ${min_projection[-1]:,.2f}")
st.markdown(f"**📈 95th Percentile (Best-Case):**\n# ${max_projection[-1]:,.2f}")
