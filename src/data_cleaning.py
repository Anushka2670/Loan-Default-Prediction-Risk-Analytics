from pathlib import Path
import pandas as pd

# LOAD DATASET 

BASE_DIR = Path(__file__).resolve().parent.parent
csv_path = BASE_DIR/ "data" / "credit_risk_dataset.csv"
df = pd.read_csv(csv_path)
print("Original Shape:", df.shape)

# MISSING VALUE TREATMENT 

# loan_int_rate -> median by loan_grade

df["loan_int_rate"] = (
    df.groupby("loan_grade")["loan_int_rate"]
        .transform(lambda x: x.fillna(x.median()))
)

# person_emp_length -> median by loan_intent

df["person_emp_length"] = (
    df.groupby("loan_intent")["person_emp_length"]
        .transform(lambda x: x.fillna(x.median()))
)

# OUTLIER TREATMENT

df["person_age"] = df["person_age"].clip(upper=80)

df["person_emp_length"] = (
    df["person_emp_length"].clip(upper=50)
)

#VALIDATION

print("\nMissing Values After Cleaning:\n")
print(df.isnull().sum())

print("\nMaximum Age:", df["person_age"].max())
print("Maximum Employment Length:", df["person_emp_length"].max())

# SAVE CLEAN DATASET

clean_path = BASE_DIR/ "data" / "credit_risk_cleaned.csv"
df.to_csv(clean_path, index = False)

print("\nCleaned File Saved:")
print(clean_path)
