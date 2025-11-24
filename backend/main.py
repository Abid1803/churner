from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import pickle
import numpy as np
import pandas as pd

# load files
model = pickle.load(open("model.pkl", "rb"))
scaler = pickle.load(open("scaler.pkl", "rb"))
features = pickle.load(open("features.pkl", "rb"))

app = FastAPI()

# CORS FIX
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # allow all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# INPUT FORMAT users will send
class UserInput(BaseModel):
    gender: str
    SeniorCitizen: int
    Partner: str
    Dependents: str
    tenure: int
    PhoneService: str
    MultipleLines: str
    InternetService: str
    OnlineSecurity: str
    OnlineBackup: str
    DeviceProtection: str
    TechSupport: str
    StreamingTV: str
    StreamingMovies: str
    Contract: str
    PaperlessBilling: str
    PaymentMethod: str
    MonthlyCharges: float
    TotalCharges: float


# PREPROCESSING FUNCTION
def preprocess(data: dict):

    df = pd.DataFrame([data])

    # binary mapping
    bin_cols = ["Partner", "Dependents", "PhoneService", "PaperlessBilling"]
    for col in bin_cols:
        df[col] = df[col].map({"Yes": 1, "No": 0})

    # total charges fix
    df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")
    df["TotalCharges"].fillna(df["TotalCharges"].median(), inplace=True)

    # get dummy variables
    df = pd.get_dummies(df, drop_first=True)

    # align columns with training features
    df = df.reindex(columns=features, fill_value=0)

    # scale
    scaled = scaler.transform(df)

    return scaled


@app.get("/")
def home():
    return {"message": "Churn Prediction API is running"}


@app.post("/predict")
def predict(user: UserInput):

    processed = preprocess(user.dict())
    prob = model.predict_proba(processed)[0][1]

    return {"churn_probability": float(prob)}
