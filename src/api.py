from fastapi import FastAPI
from src.shap_analysis import explain_loan
from src.score_loader import save_score
from pydantic import BaseModel
from src.score_loader import save_score
import joblib
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

model = joblib.load(
    "models/loan_default_model.pkl"
)

class LoanInput(BaseModel):

    loan_id: int
    person_age:int
    person_income:int
    person_home_ownership:str
    person_emp_length:int
    loan_intent:str
    loan_grade:str
    loan_amnt:int
    loan_int_rate:float
    loan_percent_income:float
    cb_person_default_on_file:str
    cb_person_cred_hist_length:int

def get_risk(prob):

    if prob < 0.20:
        return "LOW"

    elif prob < 0.50:
        return "MEDIUM"

    elif prob < 0.80:
        return "HIGH"

    return "VERY_HIGH"

@app.get("/")
def home():

    return {
        "message":
        "Loan Default Prediction API Running"
    }

@app.post("/predict")
def predict(data: LoanInput):

    df = pd.DataFrame([data.model_dump()])

    df = df.drop(
        columns=["loan_id"]
    )

    df = pd.get_dummies(df)
    
    model_columns = model.feature_names_in_

    df = df.reindex(
        columns=model_columns,
        fill_value=0
    )

    prediction = model.predict(df)[0]

    probability = model.predict_proba(df)[0][1]

    risk_tier = get_risk(probability)

    explanation = explain_loan(data.model_dump(exclude={"loan_id"}))

    top_factors = []

    for _, row in explanation.iterrows():

        top_factors.append({
            "feature": row["feature"],
            "shap_value": round(
                float(row["shap_value"]),
                4
            )
    })

    save_score(
    loan_id=data.loan_id,
    probability=round(
        float(probability),
        3
    ),
    risk_tier=risk_tier
    )

    return {

        "prediction":int(prediction),

        "default_probability":round(float(probability), 3),

        "risk_tier": risk_tier,
        "top_factors": top_factors
    }