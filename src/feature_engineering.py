import pandas as pd

df = pd.read_csv("data\credit_risk_cleaned.csv")

# Target
y = df["loan_status"]

# Feature
X = df.drop("loan_status", axis = 1)

# Encode categoricals
categorical = [
    "person_home_ownership",
    "loan_intent",
    "loan_grade",
    "cb_person_default_on_file"
]

X = pd.get_dummies(
    X,
    columns= categorical,
    drop_first=True
)

print("Feature Shape:")
print(X.shape)

print("\nFirst Columns:")
print(X.columns.tolist()[:20])