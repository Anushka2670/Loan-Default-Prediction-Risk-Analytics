import pandas as pd

df = pd.read_csv("data\credit_risk_cleaned.csv")

print("\n========== SUMMARY ==========")
print(df.describe())

print("\n========== DEFAULT RATE ==========")

default_rate = (
    df["loan_status"].mean()*100
)

print(f"{default_rate:.2f}%")

print("\n========== LOAN STATUS ==========")
print(df["loan_status"].value_counts())

print("\n========== GRADE ==========")
print(df["loan_grade"].value_counts())

print("\n========== HOME OWNERSHIP ==========")
print(df["person_home_ownership"].value_counts())