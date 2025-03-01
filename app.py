import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/predict"

# Title
st.title("🚗 Car Price Prediction")
st.markdown("### Enter car details to estimate its price.")

# Car Model
model = st.selectbox("Select Car Model", ["Kia", "Mercedes-Benz", "Nissan", "Toyota"])

# Year
year = st.number_input("Year of Manufacture", min_value=1987, max_value=2025, step=1, value=2018)

# Motor Type
motor_type = st.selectbox("Select Motor Type", ["Petrol", "Diesel", "Hybrid", "Electric"])

# Running Distance
running = st.number_input("Mileage/Running Distance", min_value=0, step=5000, value=50000)
unit = st.selectbox("Unit", ["km", "miles"])
running_text = f"{running} {unit}"

# Wheel Position
wheel = st.selectbox("Wheel Position", ["Left", "Right"])

# Car Color
color = st.selectbox(
    "Select Car Color",
    ["Black", "White", "Silver", "Skyblue", "Golden", "Blue", "Brown", "Cherry", "Clove", "Gray",
     "Green", "Orange", "Other", "Pink", "Purple", "Red"]
)

# Car Type
car_type = st.selectbox("Select Car Type", ["Sedan", "SUV", "Universal", "Hatchback", "Minivan / Minibus", "Pickup"])

# Car Status
status = st.selectbox("Select Car Condition", ["Excellent", "Good", "Normal", "Bad", "Very Bad"])

# Motor Volume
motor_volume = st.number_input("Motor Volume (Liters)", min_value=0.5, max_value=6.0, step=0.1, value=2.0)

# Prediction Button
if st.button("Predict Price"):
    input_data = {
        "model": model.lower(),  # Convert to lowercase to match API
        "year": year,
        "motor_type": motor_type.lower(),
        "running": running_text,
        "wheel": wheel.lower(),
        "color": color.lower(),
        "type": car_type.lower(),
        "status": status.lower(),
        "motor_volume": motor_volume,
    }

    try:
        response = requests.post(API_URL, json=input_data)
        result = response.json()

        if "predicted_price" in result:
            st.success(f"🚘 Estimated Price: ${result['predicted_price']:,.2f}")
        else:
            st.error(result["error"])
    except requests.exceptions.RequestException as e:
        st.error(f"❌ API request failed: {e}")
