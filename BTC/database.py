import sqlite3 as sl

conn = sl.connect('BTC/BTC_Database.db')

print("Opened database successfully")

#conn.execute('''CREATE TABLE BALANCE_SHEET
            # (ID INT PRIMARY KEY     NOT NULL,
            #     BALANCE            FLOAT   NOT NULL
            # );''')
#print("Table created successfully")

#conn.commit()

#conn.execute('UPDATE BALANCE_SHEET set BALANCE = 1 where ID = ##################')
#conn.execute('UPDATE BALANCE_SHEET set BALANCE = 1 where ID = ##################')
#conn.execute('UPDATE BALANCE_SHEET set BALANCE = 1 where ID = ##################')
#conn.execute('UPDATE BALANCE_SHEET set BALANCE = 1 where ID = ##################')
#conn.execute('UPDATE BALANCE_SHEET set BALANCE = 1 where ID = ##################')
conn.execute('''INSERT INTO BALANCE_SHEET (BALANCE, ID)
VALUES (1, ##################)''')


conn.commit()

conn.close()
