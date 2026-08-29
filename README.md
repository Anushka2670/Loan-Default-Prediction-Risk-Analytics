# Loan Default Prediction & Risk Analytics System

----------- About the Project -----------

This project is a machine learning based loan risk prediction system. The main goal is to predict whether a loan applicant is likely to default and assign a risk level based on the predicted probability.

I built the project as an end-to-end system rather than keeping the model as a standalone Python program. The project includes data processing, model training, Oracle database integration, a FastAPI prediction API, and a Power BI dashboard.

----------- What the Project Does -----------

The system takes loan and applicant information such as loan ID, income, age, loan amount, interest rate, loan grade, home ownership and credit history.

The trained LightGBM model then:

1. Predicts whether the loan is likely to default.
2. Calculates the probability of default.
3. Assigns a risk tier based on the probability.
4. Stores the prediction and risk score in Oracle.
5. Makes the stored data available for Power BI analysis.

----------- Technologies Used -----------

-> Python
-> Pandas
-> Scikit-learn
-> LightGBM
-> Joblib
-> FastAPI
-> Uvicorn
-> Oracle Database
-> SQL
-> Power BI

----------- Machine Learning -----------

I used Logistic Regression as a baseline model and LightGBM as the main model.

The target variable is `loan_status`:

`0` - No Default
`1` - Default

The final LightGBM model was trained with class balancing because the dataset contains more non-default cases than default cases.

----------- Model Results -----------

The current LightGBM model produced the following results on the test data:

| Metric    | Result |
| --------- | ------ |
| Accuracy  | 91.64% |
| Precision | 81.29% |
| Recall    | 80.90% |
| F1 Score  | 81.10% |
| ROC-AUC   | 94.87% |

Confusion matrix:

[[4803  269]
 [ 276 1169]]

The trained model is saved as:

"models/loan_default_model.pk1"

----------- Risk Tiers -----------

The model's default probability is converted into four risk categories:

| Default Probability | Risk Tier |
| ------------------- | --------- |
| Below 20%           | LOW       |
| 20% to below 50%    | MEDIUM    |
| 50% to below 80%    | HIGH      |
| 80% or above        | VERY_HIGH |

For example, during API testing, one applicant received:

"prediction": 1,
"default_probability": 0.549,
"risk_tier": HIGH

Here, `1` means the model predicted a default.

----------- FastAPI -----------

I created a FastAPI application to use the trained model for individual loan predictions.

The main endpoint is:

POST /predict

The API accepts applicant information and returns the prediction, default probability and risk tier.

The API returns:

- Prediction
- Default probability
- Risk tier

The prediction is also stored in the Oracle 'RISK_SCORES' table using the provided loan ID.

To start the API:

uvicorn src.api:app --reload

Swagger can then be opened at:

http://127.0.0.1:8000/docs

This allows loan information to be entered manually and the prediction to be tested.

----------- Oracle Database -----------

Oracle is used to store the loan information and model scoring results.

The `RISK_SCORES` table stores information such as:

-> Loan ID
-> Default probability
-> Risk tier
-> Model version
-> Scoring time

The API prediction is saved to Oracle using the loan ID provided in the request.

I also created an Oracle view called:

VW_RISK_ANALYTICS

This view combines the loan information with the model scores and is used as the source for the Power BI dashboard.

----------- Power BI Dashboard -----------

The Power BI dashboard is connected to the Oracle analytics view.

The dashboard currently contains:

-> Total Loan Applications
-> Average Default Probability
-> Average Interest Rate
-> High Risk Loan Count
-> Risk Tier Distribution
-> Default Risk by Loan Grade

The dashboard is saved in the `dashboard` folder.

----------- Project Structure -----------

Loan Default Prediction & Risk Analytics System/
│
├── dashboard/
│   └── loan_prediction_dashboard.pbix
|
├── data/
|   ├── credit_risk_dataset.csv
│   └── credit_risk_cleaned.csv
│
├── models/
│   └── loan_default_model.pkl
|
├── sql/
|   ├── create_remaining_tables.sql
|   ├── create_tables.sql
│   └── eda_queries.sql
│
├── src/
│   ├── api.py
│   ├── batch_score.py
|   ├── bulk_loader.py
|   ├── data_check.py
|   ├── data_cleaning.py
|   ├── eda_analysis.py
|   ├── feature_engineering.py
│   ├── score_loader.py
|   ├── test_connection.py
│   └──train_model.py
│
├── requirements.txt
└── README.md

----------- Running the Project -----------

1. Create the virtual environment

python -m venv venv

2. Activate it on Windows

venv\Scripts\Activate.ps1

3. Install the required packages

pip install -r requirements.txt

4. Make sure Oracle Database is running

The project currently uses the Oracle service:

localhost:1521/XEPDB1

5. Start the FastAPI application

uvicorn src.api:app --reload

6. Test the API

Open:
http://127.0.0.1:8000/docs

Use `POST /predict` to enter loan applicant details.

----------- Project Flow -----------

The complete flow of the project is:

Loan Dataset
     ↓
Data Cleaning
     ↓
Feature Preparation
     ↓
LightGBM Model Training
     ↓
FastAPI
     ↓
Prediction + Default Probability
     ↓
Risk Tier
     ↓
Oracle Database
     ↓
Oracle Analytics View
     ↓
Power BI Dashboard

----------- Future Improvements -----------

Some improvements I would like to add later are:

-> SHAP based model explanations
-> Better model monitoring
-> API authentication
-> Automated model retraining
-> Cloud deployment
-> Automated Power BI refresh

----------- Project Status -----------

The main end-to-end workflow is completed and working locally.
The current system can:

- Clean and prepare the loan dataset.
- Train and evaluate a LightGBM model.
- Generate individual loan prediction through FastAPI.
- Calculate default probability and risk tier.
- Store API scoring results in Oracle.
- Provide an Oracle analytics view.
- Display risk analytics through Power BI.