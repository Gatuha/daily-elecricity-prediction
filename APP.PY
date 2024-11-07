import streamlit as st
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
from joblib import load  # Import joblib for model serialization

# Sample function to generate prediction (replace with actual implementation)
def generate_prediction(start_date, end_date, location, bank_holiday):
    # Load the trained model
    trained_model = load('/workspaces/electricity-demand-deployment/model/sarima_model1.pkl')  # Load the model
    
    # Sample prediction generation (replace with your model logic)
    # Here, we'll just demonstrate how bank holiday affects demand (you'll need to adjust this logic)
    if bank_holiday:
        demand_modifier = 0.8  # Reducing demand by 20% on bank holidays
    else:
        demand_modifier = 1.0  # No modification if it's not a bank holiday
    
    prediction_df = pd.DataFrame({
        'Date': pd.date_range(start_date, end_date),
        'Electricity Demand (MW)': trained_model.predict(start=start_date, end=end_date) * demand_modifier
    })
    
    # Set index as numbering
    prediction_df.index = range(1, len(prediction_df) + 1)
    return prediction_df

# Streamlit app code
def main():
    st.title("Electricity Demand Forecasting")

    # Sidebar with user input components
    st.sidebar.title("Settings")
    start_date = st.sidebar.date_input("Start Date", value=datetime.now())
    end_date = st.sidebar.date_input("End Date", value=datetime.now())
    location = st.sidebar.selectbox("Location", ["Location A", "Location B", "Location C"])  # Sample locations
    bank_holiday = st.sidebar.checkbox("Bank Holiday")  # Checkbox to indicate whether it's a bank holiday or not
    
    # Button to trigger prediction
    if st.sidebar.button("Predict", key="predict_button"):
        # Call function to generate prediction based on user inputs
        prediction_df = generate_prediction(start_date, end_date, location, bank_holiday)
        
        # Display prediction results
        st.subheader("Electricity Demand Prediction")
        st.write(prediction_df)
        
        # Check if the selected date range is exactly one week (7 days)
        if (end_date - start_date).days >= 7:
            # Plot the predicted demand over time
            plt.figure(figsize=(10, 6))
            plt.plot(prediction_df['Date'], prediction_df['Electricity Demand (MW)'], marker='o', color='b', linestyle='-')
            plt.title("Predicted Electricity Demand Over Time", fontsize=16)
            plt.xlabel("Date", fontsize=14)
            plt.ylabel("Electricity Demand (MW)", fontsize=14)
            plt.xticks(rotation=45)
            plt.grid(True, linestyle='--', alpha=0.5)
            st.pyplot(plt)
        else:
            st.warning("Prediction can only be plotted if the selected date range is equal to or more than one week (7 days).")

if __name__ == "__main__":
    main()
