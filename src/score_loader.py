from datetime import datetime
import cx_Oracle
import os
from dotenv import load_dotenv

load_dotenv()

def save_score(
    loan_id,
    probability,
    risk_tier
):

    connection = cx_Oracle.connect(
        os.getenv("ORACLE_USER"),
        os.getenv("ORACLE_PASSWORD"),
        os.getenv("ORACLE_DSN")
    )

    cursor = connection.cursor()

    cursor.execute(
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
            loan_id,
            probability,
            risk_tier,
            "LIGHTGBM_V1",
            datetime.now()
        ]
    )

    connection.commit()

    cursor.close()
    connection.close()

    print("Score Saved")