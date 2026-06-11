from datetime import datetime
import pandas as pd
import cx_Oracle

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier


# CONNECT

connection = cx_Oracle.connect(
    "RISK_USER/risk123@localhost:1521/XEPDB1"
)
cursor = connection.cursor()

# LOAD

df = pd.read_csv(
    "data/credit_risk_cleaned.csv"
)

# TARGET

y = df["loan_status"]

X = df.drop(
    "loan_status",
    axis=1
)

# ENCODE

categorical = [
    "person_home_ownership",
    "loan_intent",
    "loan_grade",
    "cb_person_default_on_file"
]

X = pd.get_dummies(
    X,
    columns=categorical,
    drop_first=True
)

# SPLIT

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# MODEL

model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

model.fit(
    X_train,
    y_train
)

# SCORE

prob = model.predict_proba(
    X_test
)[:,1]

def get_risk_tier(p):

    if p < 0.20:
        return "LOW"

    elif p < 0.50:
        return "MEDIUM"

    elif p < 0.80:
        return "HIGH"

    return "VERY_HIGH"


loan_ids = list(
    range(
        1,
        len(prob)+1
    )
)

insert_sql = """
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
"""

count = 0

for i in range(len(prob)):

    cursor.execute(
        insert_sql,
        [
            loan_ids[i],
            round(float(prob[i]),4),
            get_risk_tier(prob[i]),
            "RF_V1",
            datetime.now()
        ]
    )

    count += 1

    if count % 1000 == 0:

        connection.commit()

        print(
            f"{count} scores stored"
        )
connection.commit()

print("\nDone")

cursor.close()
connection.close()