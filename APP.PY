import streamlit as st
import pandas as pd
import numpy as np
import pickle
from datetime import datetime, timedelta

# Load the trained model
with open("model/sarima_model.pkl", "rb") as file:
    sarima_model = pickle.load(file)

# Title and description
st.title("Electricity Demand Forecasting")
st.write("This app predicts future electricity demand using a SARIMA model.")

# Input selection for forecast period
st.subheader("Forecast Configuration")
forecast_days = st.slider("Select number of days for forecast:", 1, 30, 7)

# Load and display the latest data if needed
# Optional: Load any recent data for reference
# data = pd.read_csv("data/africa_grid.csv")
# st.write(data.tail())

# Forecasting
st.subheader("Forecast Results")
# Generate the forecast
forecast = sarima_model.forecast(steps=forecast_days)
dates = [datetime.now() + timedelta(days=i) for i in range(forecast_days)]

# Display forecast
forecast_df = pd.DataFrame({"Date": dates, "Forecasted Demand": forecast})
st.line_chart(forecast_df.set_index("Date"))

# Display forecast values in a table
st.write(forecast_df)
