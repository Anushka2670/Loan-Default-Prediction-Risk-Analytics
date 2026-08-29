import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from lightgbm import LGBMClassifier
import joblib
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix,
    classification_report
)

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

# BASELINE

baseline = LogisticRegression(
    max_iter=5000,
    class_weight="balanced"
)

baseline.fit(
    X_train,
    y_train
)

baseline_pred = baseline.predict(X_test)

print("\nLogistic Accuracy:")

print(
    accuracy_score(
        y_test,
        baseline_pred
    )
)

# FINAL MODEL

model = LGBMClassifier(
    n_estimators=300,
    learning_rate=0.05,
    max_depth=8,
    class_weight="balanced",
    random_state=42
)

model.fit(
    X_train,
    y_train
)

# EVALUATION

model_pred = model.predict(X_test)
model_prob = model.predict_proba(X_test)[:, 1]

print("\nLightGBM Evaluation")

print("Accuracy:",
      accuracy_score(y_test, model_pred))

print("Precision:",
      precision_score(y_test, model_pred))

print("Recall:",
      recall_score(y_test, model_pred))

print("F1 Score:",
      f1_score(y_test, model_pred))

print("ROC-AUC:",
      roc_auc_score(y_test, model_prob))

print("\nConfusion Matrix:")
print(confusion_matrix(y_test, model_pred))

print("\nClassification Report:")
print(classification_report(y_test, model_pred))

joblib.dump(
    model,
    "models/loan_default_model.pkl"
)

print("\nModel Saved")