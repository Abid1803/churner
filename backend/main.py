from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import pickle
import pandas as pd

# Load model artifacts
model = pickle.load(open("model.pkl", "rb"))
scaler = pickle.load(open("scaler.pkl", "rb"))
features = pickle.load(open("features.pkl", "rb"))

app = FastAPI()

# Allow all frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
#example push
# Input schema
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

# Preprocessing
def preprocess(data):
    df = pd.DataFrame([data])

    binary_cols = ["Partner", "Dependents", "PhoneService", "PaperlessBilling"]
    for col in binary_cols:
        df[col] = df[col].map({"Yes": 1, "No": 0})

    df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")
    df["TotalCharges"].fillna(df["TotalCharges"].median(), inplace=True)

    df = pd.get_dummies(df, drop_first=True)

    df = df.reindex(columns=features, fill_value=0)

    scaled = scaler.transform(df)
    return scaled

@app.get("/")
def home():
    return {"message": "Churn Prediction API is running from GitHub → HuggingFace Sync"}

@app.post("/predict")
def predict(user: UserInput):
    processed = preprocess(user.dict())
    probability = model.predict_proba(processed)[0][1]
    return {"churn_probability": float(probability)}
