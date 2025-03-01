import streamlit as st
import requests

# FastAPI endpoint
API_URL = "http://127.0.0.1:8000/predict"

# Title
st.title("🚗 Car Price Prediction")
st.markdown("### Enter the details of the car to estimate its price.")

# Car Model
model = st.selectbox("Select Car Model", ["Toyota", "Mercedes-Benz", "Kia", "Nissan", "Hyundai"])

# Year
year = st.number_input("Year of Manufacture", min_value=1987, max_value=2025, step=1, value=2018)

# Motor Type
motor_type = st.selectbox("Select Motor Type", ["Petrol", "Gas", "Diesel", "Electric"])

# Running (Distance Covered)
running = st.number_input("Mileage/Running Distance", min_value=0, step=5000, value=50000)
unit = st.selectbox("Unit", ["km", "miles"])

# Convert miles to km if necessary
if unit == "miles":
    running = running * 1.609

# Wheel Position
wheel = st.selectbox("Wheel Position", ["Left", "Right"])

# Car Color
color = st.selectbox("Select Car Color", ["Black", "White", "Silver", "Blue", "Gray", "Other"])

# Car Type
car_type = st.selectbox("Select Car Type", ["Sedan", "SUV", "Minivan / Minibus", "Pickup", "Universal"])

# Car Status (Condition)
status = st.selectbox("Select Car Condition", ["Excellent", "Good", "Normal", "Crashed"])

# Motor Volume
motor_volume = st.number_input("Enter Motor Volume (e.g., 2.0, 3.2)", min_value=0.5, max_value=6.0, step=0.1, value=2.0)

# Prediction Button
if st.button("Predict Price 💰"):
    # Prepare data for API request
    input_data = {
        "model": model,
        "year": year,
        "motor_type": motor_type,
        "running": running,
        "wheel": wheel.lower(),
        "color": color,
        "type": car_type,
        "status": status,
        "motor_volume": motor_volume
    }

    # Call FastAPI endpoint
    try:
        response = requests.post(API_URL, json=input_data)
        if response.status_code == 200:
            predicted_price = response.json()["price"]
            st.success(f"💰 Predicted Car Price: ${predicted_price:,.2f}")
        else:
            st.error("Error: Unable to fetch prediction from API.")
    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to API: {e}")
