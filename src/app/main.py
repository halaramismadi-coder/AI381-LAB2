import pandas as pd
from pathlib import Path

import joblib
from fastapi import FastAPI
from pydantic import BaseModel, Field

# Find the project root and load the trained model.
PROJECT_ROOT = Path(__file__).resolve().parents[2]
MODEL_PATH = PROJECT_ROOT / "model.joblib"
model = joblib.load(MODEL_PATH)

app = FastAPI(title="Customer Churn Prediction API")


class CustomerInput(BaseModel):
    tenure_months: int = Field(ge=0)
    monthly_charges: float = Field(ge=0)
    contract: str
    internet_service: str
    support_calls: int = Field(ge=0)


@app.get("/health")
def health():
    return {"status": "healthy", "model_loaded": True}



@app.post("/predict")
def predict(customer: CustomerInput):
    customer_data = customer.model_dump()

    # Convert the customer dictionary into a 2D DataFrame
    customer_df = pd.DataFrame([customer_data])

    prediction = int(model.predict(customer_df)[0])
    probability = float(model.predict_proba(customer_df)[0][1])

    return {
        "churn_prediction": prediction,
        "churn_probability": round(probability, 4),
    }
