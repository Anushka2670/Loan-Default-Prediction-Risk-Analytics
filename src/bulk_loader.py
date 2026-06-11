from pathlib import Path
from datetime import datetime, timedelta
import random
import pandas as pd
import cx_Oracle

# CONFIGURATION

USERNAME = "RISK_USER"
PASSWORD = "risk123"          

CONNECT_STRING = "RISK_USER/risk123@localhost:1521/XEPDB1"

BATCH_SIZE = 1000

# LOAD CLEAN DATA

BASE_DIR = Path(__file__).resolve().parent.parent

csv_path = BASE_DIR / "data" / "credit_risk_cleaned.csv"

df = pd.read_csv(csv_path)

print(f"Rows Loaded From CSV: {len(df)}")

# GENERATE ISSUE DATE

start_date = datetime(2020, 1, 1)
end_date = datetime(2023, 12, 31)

days_between = (end_date - start_date).days

df["issue_date"] = [
    start_date + timedelta(days=random.randint(0, days_between))
    for _ in range(len(df))
]

print("Issue Dates Generated")

# CONNECT TO ORACLE

connection = None

try:

    connection = cx_Oracle.connect(CONNECT_STRING)
    connection.autocommit = False
    cursor = connection.cursor()

    cursor.execute("""
    SELECT
    SYS_CONTEXT('USERENV','DB_NAME'),
    SYS_CONTEXT('USERENV','SERVICE_NAME')
    FROM dual
    """)

    print("Python DB:")
    print(cursor.fetchone())

    print("Connected To Oracle")

    borrower_sql = """
    INSERT INTO borrowers
    (
    person_income,
    person_emp_length,
    person_home_ownership,
    cb_person_default_on_file,
    cb_person_cred_hist_length,
    person_age
    )
    VALUES
    (
    :1,:2,:3,:4,:5,:6
    )
    """

    loan_sql = """
    INSERT INTO loans
    (
        borrower_id,
        loan_amnt,
        loan_int_rate,
        loan_grade,
        loan_intent,
        loan_status,
        issue_date,
        loan_percent_income
    )
    VALUES
    (
        :1,:2,:3,:4,:5,:6,:7,:8
    )
    """

    count = 0

    for index, row in df.iterrows():

        try:

            # Insert borrower
            cursor.execute(
                borrower_sql,
                [
                    float(row["person_income"]),
                    float(row["person_emp_length"]),
                    str(row["person_home_ownership"]),
                    str(row["cb_person_default_on_file"]),
                    int(row["cb_person_cred_hist_length"]),
                    int(row["person_age"])
                ]
            )

            # Get borrower id
            cursor.execute(
                """
                SELECT MAX(borrower_id)
                FROM borrowers
                """
            )

            new_borrower_id = cursor.fetchone()[0]

            # Insert loan
            cursor.execute(
                loan_sql,
                [
                    int(new_borrower_id),
                    float(row["loan_amnt"]),
                    float(row["loan_int_rate"]),
                    str(row["loan_grade"]),
                    str(row["loan_intent"]),
                    int(row["loan_status"]),
                    row["issue_date"],
                    float(row["loan_percent_income"])
                ]
            )

            count += 1

            if count % 1000 == 0:
                connection.commit()
                print(f"{count} rows committed")

        except Exception as row_error:

            print("\nFAILED AT ROW:", index + 1)
            print(row_error)
            break

    connection.commit()

    cursor.execute("""
    SELECT COUNT(*)
    FROM borrowers
    """)

    print("DB Borrowers:", cursor.fetchone()[0])

    cursor.execute("""
    SELECT COUNT(*)
    FROM loans
    """)

    print("DB Loans:", cursor.fetchone()[0])

    verify_conn = cx_Oracle.connect(CONNECT_STRING)

    verify_cursor = verify_conn.cursor()

    verify_cursor.execute(
    """
    SELECT COUNT(*)
    FROM borrowers
    """
    )

    print(
    "NEW CONNECTION Borrowers:",
    verify_cursor.fetchone()[0]
    )

    verify_cursor.execute(
    """
    SELECT COUNT(*)
    FROM loans
    """
    )

    print(
    "NEW CONNECTION Loans:",
    verify_cursor.fetchone()[0]
    )

    verify_conn.close()

except Exception as e:

    print("ERROR OCCURRED")
    print(e)

finally:

    if connection:
        connection.close()
        print("Oracle Connection Closed")