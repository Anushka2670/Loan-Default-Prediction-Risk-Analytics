import cx_Oracle 

try:
    connection = cx_Oracle.connect(
         "Risk_User/risk123@localhost:1521/XEPDB1"
   )
    
    print("Connected Successfully")
    cursor = connection.cursor()
    cursor.execute("SELECT USER FROM dual")
    print(cursor.fetchone())

except Exception as e:
    print("Error:", e)


finally:
    if 'connection' in locals():
        connection.close()
        print("Connection Closed")