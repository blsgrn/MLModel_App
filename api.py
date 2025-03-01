import pickle
from fastapi import FastAPI
from pydantic import BaseModel

# Load model
model_path = r"/home/balasegaran/Documents/gbr_model.pkl"
try:
    model = pickle.load(open(model_path, 'rb'))
except Exception as e:
    print(f"Error loading model: {e}")

# FastAPI app instance
app = FastAPI(
    title="Car Price Prediction API",
    description="API for price prediction of car",
    version="1.0.0",
    contact={
        "student_id": "st20242846",
        "email": "blsgrn@tutanota.com",
    }
)


# Request Model
class CarFeatures(BaseModel):
    model: str
    year: int
    motor_type: str
    running: float
    wheel: str
    color: str
    type: str
    status: str
    motor_volume: float


@app.get("/")
def read_root():
    return {"message": "Car Prediction API"}


@app.post("/predict")
def predict_price(car: CarFeatures):
    # Convert inputs into a format suitable for the model (modify this based on your preprocessing)
    features = [[
        car.year,
        car.motor_volume,
        car.running  # Already converted to km in Streamlit
    ]]

    # Make prediction
    predicted_price = model.predict(features)[0]

    return {"price": predicted_price}
