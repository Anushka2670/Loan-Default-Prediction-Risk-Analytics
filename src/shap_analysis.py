import pandas as pd
import shap
import joblib
import matplotlib.pyplot as plt

# LOAD DATA
df = pd.read_csv("data/credit_risk_cleaned.csv")

# TARGET
X = df.drop("loan_status", axis=1)

# ENCODE
X = pd.get_dummies(X)

# LOAD MODEL
model = joblib.load("models/loan_default_model.pkl")

# MATCH TRAINING FEATURES EXACTLY
model_columns = model.feature_names_in_

X = X.reindex(columns=model_columns, fill_value=0)

# SHAP EXPLAINER
explainer = shap.TreeExplainer(model)

shap_values = explainer.shap_values(X)

# HANDLE SHAP OUTPUT
if isinstance(shap_values, list):
    shap_values = shap_values[1]

# SUMMARY PLOT
shap.summary_plot(shap_values, X, show=False)

plt.tight_layout()

plt.savefig(
    "reports/shap_summary.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()

print("SHAP summary plot saved.")
print("Features used:", X.shape[1])

# SHAP FEATURE IMPORTANCE
importance = pd.DataFrame({
    "feature": X.columns,
    "importance": abs(shap_values).mean(axis=0)
})

importance = importance.sort_values(
    "importance",
    ascending=False
)

plt.figure(figsize=(10, 7))

plt.barh(
    importance["feature"].head(10)[::-1],
    importance["importance"].head(10)[::-1]
)

plt.xlabel("Mean |SHAP Value|")
plt.title("Top 10 Features Influencing Loan Default Prediction")

plt.tight_layout()

plt.savefig(
    "reports/shap_feature_importance.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()

print("SHAP feature importance saved.")

def explain_loan(loan_data):
    """
    Generate SHAP explanation for one loan.
    """

    # Convert input to DataFrame
    loan_df = pd.DataFrame([loan_data])

    # Encode categorical variables
    loan_df = pd.get_dummies(loan_df)

    # Match model features exactly
    loan_df = loan_df.reindex(columns=model_columns, fill_value=0)

    # Calculate SHAP values
    values = explainer.shap_values(loan_df)

    if isinstance(values, list):
        values = values[1]

    # Get feature contributions
    contributions = pd.DataFrame({
        "feature": loan_df.columns,
        "shap_value": values[0]
    })

    # Sort by absolute contribution
    contributions["abs_value"] = (
        contributions["shap_value"].abs()
    )

    contributions = contributions.sort_values(
        "abs_value",
        ascending=False
    )

    return contributions.head(5)

if __name__ == "__main__":

    test_loan = {
        "person_age": 30,
        "person_income": 40000,
        "person_home_ownership": "RENT",
        "person_emp_length": 3,
        "loan_intent": "EDUCATION",
        "loan_grade": "B",
        "loan_amnt": 10000,
        "loan_int_rate": 10.5,
        "loan_percent_income": 0.25,
        "cb_person_default_on_file": "N",
        "cb_person_cred_hist_length": 3
    }

    result = explain_loan(test_loan)

    print("\nTop factors affecting this prediction:")
    print(result[["feature", "shap_value"]])