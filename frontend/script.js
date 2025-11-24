const API_URL = "https://your-render-url.onrender.com/predict";

async function predict() {

  const data = {
    gender: document.getElementById("gender").value,
    SeniorCitizen: Number(document.getElementById("SeniorCitizen").value),
    Partner: document.getElementById("Partner").value,
    Dependents: document.getElementById("Dependents").value,
    tenure: Number(document.getElementById("tenure").value),
    PhoneService: document.getElementById("PhoneService").value,
    MultipleLines: document.getElementById("MultipleLines").value,
    InternetService: document.getElementById("InternetService").value,
    OnlineSecurity: document.getElementById("OnlineSecurity").value,
    OnlineBackup: "No",            // you can add all remaining fields
    DeviceProtection: "No",
    TechSupport: "No",
    StreamingTV: "No",
    StreamingMovies: "No",
    Contract: "Month-to-month",
    PaperlessBilling: "Yes",
    PaymentMethod: "Electronic check",
    MonthlyCharges: Number(document.getElementById("MonthlyCharges").value),
    TotalCharges: Number(document.getElementById("TotalCharges").value)
  };

  const res = await fetch(API_URL, {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify(data),
  });

  const out = await res.json();
  document.getElementById("result").innerText =
    "Churn Probability: " + out.churn_probability.toFixed(4);
}
