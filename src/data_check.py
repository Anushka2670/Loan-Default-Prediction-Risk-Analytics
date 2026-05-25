import pandas as pd

df = pd.read_csv("data/credit_risk_dataset.csv")

print("Shape: ")
print(df.shape)

print("\nColumns:")
print(df.columns.tolist())

print("\nMissing Values:")
print(df.isnull().sum())

print("\nFirst 5 Rows:")
print(df.head())