// TABLE RISK_TIER

CREATE TABLE RISK_TIERS (
    tier_id NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    tier_name VARCHAR(20),
    prob_min NUMBER(4,2),
    prob_max NUMBER(4,2),
    recommended_action VARCHAR2(100)
);

// TABLE LOANS 

CREATE TABLE LOANS(
    loan_id NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    borrower_id NUMBER NOT NULL,
    loan_amnt NUMBER(12,2),
    loan_int_rate NUMBER(5,2),
    loan_grade VARCHAR2(2),
    loan_intent VARCHAR2(50),
    loan_status NUMBER(1),
    issue_date DATE,
    loan_percent_income NUMBER(6,4),
    
    CONSTRAINT fk_loan_borrower 
        FOREIGN KEY (borrower_id) REFERENCES borrowers(borrower_id)
)

PARTITION BY RANGE(issue_date)
(
    PARTITION p_2020 VALUES LESS THAN (DATE '2021-01-01'),
    PARTITION p_2021 VALUES LESS THAN (DATE '2022-01-01'),
    PARTITION p_2022 VALUES LESS THAN (DATE '2023-01-01'),
    PARTITION p_2023 VALUES LESS THAN (DATE '2024-01-01'),
    PARTITION p_future VALUES LESS THAN (MAXVALUE)
);

// TABLE RISK_SCORES 

CREATE TABLE RISK_SCORES(
    score_id NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    loan_id NUMBER NOT NULL,
    default_prob NUMBER(6,4),
    risk_tier VARCHAR2(20),
    model_version VARCHAR2(50),
    scored_at DATE DEFAULT SYSDATE,
    
    CONSTRAINT fk_score_loan
        FOREIGN KEY(loan_id) REFERENCES loans(loan_id)
);

//TABLE AUDIT_LOGS 

CREATE TABLE AUDIT_LOGS(
    log_id NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    loan_id NUMBER,
    action VARCHAR2(100),
    performed_by VARCHAR2(100),
    log_time DATE DEFAULT SYSDATE,
    
    CONSTRAINT fk_audit_loan
        FOREIGN KEY(loan_id) REFERENCES loans(loan_id)
);

//CREATE INDEXES 

CREATE INDEX idx_loan_grade
ON loans(loan_grade);

CREATE INDEX idx_loan_status
ON loans(loan_status);

CREATE INDEX idx_loan_int_rate
ON loans(loan_int_rate);

CREATE INDEX idx_loan_intent
ON loans(loan_intent);

CREATE INDEX idx_borrower_income
ON borrowers(person_income);
