import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix

#LOAD

df = pd.read_csv("data/credit_risk_cleaned.csv")

#TARGET

y = df["loan_status"]

#FEATURES

X = df.drop("loan_status", axis = 1)

print(df.columns.tolist())

#ENCODE

categorical = X.select_dtypes(
    include="object"
).columns.tolist()

print("\nCategorical Columns:")
print(categorical)

X = pd.get_dummies(
    X,
    columns= categorical,
    drop_first= True
)

#SPLIT

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size = 0.2,
    random_state=42
)

print("Train:", X_train.shape)
print("Test:", X_test.shape)

#MODEL

model = RandomForestClassifier(
    n_estimators=300,
    max_depth=12,
    min_samples_split=10,
    class_weight="balanced", 
    random_state=42
)

model.fit(
    X_train,
    y_train
)

pred = model.predict(X_test)

prob = model.predict_proba(X_test)
default_probability = prob[:,1]

print("\n Sample Probabilities:")
print(default_probability[:10])

def get_risk_tier(prob):
    if prob<0.20:
        return "LOW"

    elif prob<0.50:
        return "MEDIUM"
    
    elif prob<0.80:
        return "HIGH"
    
    else:
        return "VERY_HIGH"
    
risk_tier = [
    get_risk_tier(p)
    for p in default_probability
]

print("\nRisk Tier Sample:")

for i in range(10):

    print(
        round(default_probability[i],3),
        "->",
        risk_tier[i]
    )
    
print("\nAccuracy:")
print(
    accuracy_score(
        y_test,
        pred
    )
)

print("\nClassification Report: ")
print(
    classification_report(
        y_test,
        pred
    )
)

print("\nConfusion Matrix:")

print(
    confusion_matrix(
        y_test,
        pred
    )
)