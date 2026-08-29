import pandas as pd
import joblib
import cx_Oracle
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

# LOAD MODEL

model = joblib.load(
    "models/loan_default_model.pkl"
)

# LOAD DATA

df = pd.read_csv(
    "data/credit_risk_cleaned.csv"
)

X = df.drop(
    "loan_status",
    axis=1
)

# ENCODE

X = pd.get_dummies(
    X,
    drop_first=True
)

# ALIGN COLUMNS

X = X.reindex(
    columns=model.feature_names_in_,
    fill_value=0
)

# SCORE

prob = model.predict_proba(X)[:,1]


def get_risk(p):

    if p < 0.20:
        return "LOW"

    elif p < 0.50:
        return "MEDIUM"

    elif p < 0.80:
        return "HIGH"

    return "VERY_HIGH"


# ORACLE

conn = cx_Oracle.connect(
    os.getenv("ORACLE_USER"),
    os.getenv("ORACLE_PASSWORD"),
    os.getenv("ORACLE_DSN")
)

cur = conn.cursor()

count = 0

for i in range(len(prob)):

    cur.execute(
        """
        INSERT INTO RISK_SCORES
        (
            LOAN_ID,
            DEFAULT_PROB,
            RISK_TIER,
            MODEL_VERSION,
            SCORED_AT
        )
        VALUES
        (
            :1,:2,:3,:4,:5
        )
        """,
        [
            i+1,
            round(float(prob[i]),3),
            get_risk(prob[i]),
            "LIGHTGBM_V1",
            datetime.now()
        ]
    )

    count += 1

    if count % 1000 == 0:

        conn.commit()

        print(
            f"{count} scored"
        )

conn.commit()

cur.close()

conn.close()

print("\nDONE")