CREATE TABLE BORROWERS(
    borrower_id NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    person_income NUMBER(12,2),
    person_emp_length NUMBER(5,2),
    person_home_ownership VARCHAR2(20),
    cb_person_dafault_on_file CHAR(1),
    cb_person_cred_hist_length NUMBER(5),
    person_age NUMBER(3)
);

SELECT table_name FROM user_tables WHERE table_name = 'BORROWERS';