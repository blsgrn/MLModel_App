import pickle
import numpy as np
from fastapi import FastAPI
from pydantic import BaseModel
from sklearn.preprocessing import StandardScaler

# Load trained model and scaler
model_path = "gbr_model.pkl"
scaler_path = "scaler.pkl"

try:
    with open(model_path, "rb") as file:
        model = pickle.load(file)
    print("✅ Model loaded successfully!")

    with open(scaler_path, "rb") as file:
        scaler = pickle.load(file)
    print("✅ Scaler loaded successfully!")

    print("Feature Names:", model.feature_names_in_)  # Debugging feature alignment

except Exception as e:
    print(f"❌ Error loading model/scaler: {e}")
    model, scaler = None, None

# Initialize FastAPI
app = FastAPI()

# Define input schema
class CarFeatures(BaseModel):
    model: str
    year: int
    motor_type: str
    running: str
    wheel: str
    color: str
    type: str
    status: str
    motor_volume: float

# Convert running distance
def convert_running(value: str):
    try:
        num, unit = value.split()
        num = float(num)
        return num * 1.609 if unit.lower() == "miles" else num
    except:
        return np.nan

# Define category mappings
motor_type_mapping = {"petrol": 3, "diesel": 2, "hybrid": 1, "electric": 0}
status_mapping = {"excellent": 2, "good": 1, "normal": 0, "bad": 3, "very bad": 4}
wheel_mapping = {"left": 1, "right": 0}

# Expected categories from training
model_categories = ["kia", "mercedes-benz", "nissan", "toyota"]
color_categories = ["black", "blue", "brown", "cherry", "clove", "golden", "gray",
                    "green", "orange", "other", "pink", "purple", "red", "silver", "skyblue", "white"]
type_categories = ["universal", "hatchback", "minivan / minibus", "pickup", "sedan", "suv"]

@app.post("/predict")
def predict_price(car: CarFeatures):
    if model is None or scaler is None:
        return {"error": "Model or scaler not loaded"}

    # Convert running to numeric km
    running_km = convert_running(car.running)
    if np.isnan(running_km):
        return {"error": "Invalid running format!"}

    # Feature engineering
    car_age = 2025 - car.year
    car_age_km = np.log1p(car_age * running_km)

    # Encode categorical features
    numerical_features = [
        car.year,
        motor_type_mapping.get(car.motor_type.lower(), -1),
        wheel_mapping.get(car.wheel.lower(), -1),
        status_mapping.get(car.status.lower(), -1),
        car.motor_volume,
        car_age_km,
    ]

    if -1 in numerical_features:
        return {"error": "Invalid categorical input detected!"}

    # One-hot encode categorical variables
    one_hot_model = [1 if car.model.lower() == m else 0 for m in model_categories]
    one_hot_color = [1 if car.color.lower() == c else 0 for c in color_categories]
    one_hot_type = [1 if car.type.lower() == t else 0 for t in type_categories]

    # Combine all features
    final_features = np.array(numerical_features + one_hot_model + one_hot_color + one_hot_type).reshape(1, -1)

    # Debugging outputs
    print(f"🚀 Final Feature Shape: {final_features.shape}, Expected: {model.n_features_in_}")
    print(f"🚀 Final Features: {final_features}")

    # Ensure correct number of features
    if final_features.shape[1] != model.n_features_in_:
        return {"error": f"Feature count mismatch! Expected {model.n_features_in_}, got {final_features.shape[1]}"}

    # Standardize only numeric columns
    final_features[:, [0, 1, 3, 4, 5]] = scaler.transform(final_features[:, [0, 1, 3, 4, 5]])


    # Make prediction
    predicted_price = model.predict(final_features)[0]
    return {"predicted_price": round(predicted_price, 2)}
