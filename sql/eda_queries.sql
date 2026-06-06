-- DataSet Size

SELECT COUNT(*) total_loans FROM loans;

--Default Rate

SELECT ROUND (SUM(loan_status)/COUNT(*)*100, 2)
default_rate_percent FROM loans;

--Grade Distribution

SELECT loan_grade, COUNT(*) total FROM loans 
GROUP BY loan_grade ORDER BY loan_grade;

--Intent Distribution

SELECT loan_intent, COUNT(*) total FROM loans 
GROUP BY loan_intent ORDER BY total DESC;

--Average Loan Amount by Grade 

SELECT loan_grade, ROUND(AVG(loan_amnt), 2) avg_amount
FROM loans GROUP BY loan_grade ORDER BY loan_grade;