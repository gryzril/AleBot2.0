import sqlite3 as sl

def get_all_balances():
    conn = sl.connect('BTC/BTC_Database.db')
    print("Opened database successfully")
    #str = "WHERE ID=" + id

    #bal = conn.execute('''SELECT * FROM BALANCE_SHEET 
                 #'''+str)
    cursor = conn.execute("SELECT ID, BALANCE from BALANCE_SHEET")
    data = {}
    for row in cursor:
        #print("ID = " + str(row[0]))
        #print("BALANCE = " + str(row[1]))
        data[str(row[0])] = row[1]
        
    return data

def get_balance(id):
    data = get_all_balances()
    #print(data)
    balance = data.get(str(id))
    print("returning " + str(id) + "" + str(balance))
    return balance

def transfer(id, userID, amount):
    bal = float(get_balance(id))

    if(id == userID):
        return "Nice try"

    if(amount < 0):
        return "You cannot transfer a negative amount"

    if(bal < amount):
        return "You do not have enough BTC to do this"
    
    conn = sl.connect('BTC/BTC_Database.db')
    print("Opened database successfully")
    
    amount_final = amount + float(get_balance(userID))
    
    strng = 'UPDATE BALANCE_SHEET set BALANCE = ' + str(amount_final) + ' where ID = ' + str(userID)
    
    #conn.execute('UPDATE BALANCE_SHEET set BALANCE = 1 where ID = 102968905990967296')
    
    conn.execute(strng)
    
    amount_final2 = float(get_balance(id) - amount)
    
    strng2 = 'UPDATE BALANCE_SHEET set BALANCE = ' + str(amount_final2) + ' where ID = ' + str(id)
    
    conn.execute(strng2)
    
    conn.commit()

    conn.close()
    
    return "Transfer success"

    
def credit(id, amount):
    if(amount < 0):
        return "Invalid amount to credit"
    conn = sl.connect('BTC/BTC_Database.db')
    print("Opened database successfully")
    
    amount_final = amount + float(get_balance(id))
    
    strng = 'UPDATE BALANCE_SHEET set BALANCE = ' + str(amount_final) + ' where ID = ' + str(id)

    conn.execute(strng)
    conn.commit()
    conn.close()
    
    return "credit successful"
    
def debit(id, amount):
    if(amount < 0):
        return "Invalid amount to credit"
    conn = sl.connect('BTC/BTC_Database.db')
    print("Opened database successfully")
    
    amount_final = float(get_balance(id) - amount)
    
    strng = 'UPDATE BALANCE_SHEET set BALANCE = ' + str(amount_final) + ' where ID = ' + str(id)

    conn.execute(strng)
    conn.commit()
    conn.close()
    
    return "debit successful"
    
def set_balance(id, value):
    conn = sl.connect('BTC/BTC_Database.db')
    print("Setting balance")
    
    strng = 'UPDATE BALANCE_SHEET set BALANCE = ' + str(value) + ' where ID = ' + str(id)
    
    conn.execute(strng)
    conn.commit()
    conn.close()
    
    