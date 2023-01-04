import mysql.connector

def connectDatabase(host, username, password):
    global mydb
    mydb = mysql.connector.connect(
        host=host,
        user=username,
        password=password
        )
    mycursor = mydb.cursor()
    try:
        query = "USE gas"
        mycursor.execute(query)
    except:
        query = "CREATE DATABASE gas"
        mycursor.execute(query)
        query = "USE gas"
        mycursor.execute(query)


def create_table_customers():
    mycursor = mydb.cursor(buffered=True)
    mycursor.execute("SHOW TABLES")
    for x in mycursor:
        if x[0]=="customers":
            print("Table Customers already exists")
            return
    mycursor.execute("CREATE TABLE customers (customer_id int NOT NULL AUTO_INCREMENT PRIMARY KEY, \
                        customer_name VARCHAR(255), address VARCHAR(255),\
                             phone VARCHAR(255), email_id VARCHAR(255))")
    print("Created Table Customers")

def create_table_bills():
    mycursor = mydb.cursor(buffered=True)
    mycursor.execute("SHOW TABLES")
    for x in mycursor:
        if x[0]=="bills":
            print("Table Bills already exists")
            return
    mycursor.execute("CREATE TABLE bills (bill_id int NOT NULL AUTO_INCREMENT PRIMARY KEY, \
                        customer_id VARCHAR(255), bill_startdate VARCHAR(255),\
                             bill_enddate VARCHAR(255), number_of_units VARCHAR(255),\
                                bill_amount VARCHAR(255), bill_paid VARCHAR(255))")
    print("Created Table Bills")

def create_table_users():
    mycursor = mydb.cursor(buffered=True)
    mycursor.execute("SHOW TABLES")
    for x in mycursor:
        if x[0]=="users":
            print("Table Users already exists")
            return
    mycursor.execute("CREATE TABLE users (user_id int NOT NULL AUTO_INCREMENT PRIMARY KEY, \
                        username VARCHAR(255), password VARCHAR(255))")
    print("Created Table Users")

def login():
    print("-"*25)
    print("Gas Billing System")
    print("-"*25)
    username = input("Enter the username: ")
    password = input("Enter the password: ")
    query = "SELECT * FROM users WHERE username=%s and password=%s"
    vals = (username, password)
    mycursor = mydb.cursor()
    mycursor.execute(query, vals)
    result = mycursor.fetchall()
    print("-"*50)
    if len(result)==0:
        print("Invalid username and/or password")
        print("-"*50)
        return False
    else:
        print("Access Granted")
        print("-"*50)
        return True

def add_user():
    mycursor = mydb.cursor()
    username = input("Enter the username : ")
    password = input("Enter the password : ")
    vals = (username, password)
    query = "INSERT INTO users (username, password) \
         VALUES (%s, %s)"
    mycursor.execute(query, vals)

def add_customer():
    mycursor = mydb.cursor()
    customer_name = input("Enter the customer's name :")
    address = input("Enter the customer's address :")
    phone = input("Enter the customer's phone number : ")
    email_id = input("Enter the customer's email id : ")
    vals = (customer_name, address, phone, email_id)
    query = "INSERT INTO customers (customer_name, address, phone, email_id) \
         VALUES (%s, %s, %s, %s)"
    mycursor.execute(query, vals)

def generate_bill():
    mycursor = mydb.cursor()
    customer_id = input("Enter the customer id : ")
    bill_startdate = input("Enter the billing start date : ")
    bill_enddate = input("Enter the billing end date : ")
    curr_units_on_meter = int(input("Enter the current units displayed on the meter: "))
    prev_units_on_meter = int(input("Enter the previously displayed units on the meter: "))
    number_of_units = curr_units_on_meter - prev_units_on_meter
    bill_amount = 0
    curr_units = number_of_units
    if curr_units>200:
        curr_units-=200
        bill_amount+=400
    else:
        bill_amount+=2*curr_units
        curr_units=0
    
    if curr_units>300:
        curr_units-= 300
        bill_amount+=1200
    else:
        bill_amount+=4*curr_units
        curr_units=0
    
    bill_amount+=8*curr_units
    bill_paid = "No"
    vals = (customer_id, bill_startdate, bill_enddate, number_of_units, bill_amount, bill_paid)
    query = "INSERT INTO bills (customer_id, bill_startdate, bill_enddate,\
                 number_of_units, bill_amount, bill_paid) \
         VALUES (%s, %s, %s, %s, %s, %s)"
    mycursor.execute(query, vals)
    
def display_customers():
    mycursor = mydb.cursor()
    query = "SELECT * FROM customers"
    mycursor.execute(query)
    results = mycursor.fetchall()
    for res in results:
        print(results)

def display_bills():
    mycursor = mydb.cursor()
    query = "SELECT * FROM bills"
    mycursor.execute(query)
    results = mycursor.fetchall()
    for res in results:
        print(results)

def display_users():
    mycursor = mydb.cursor()
    query = "SELECT * FROM users"
    mycursor.execute(query)
    results = mycursor.fetchall()
    for res in results:
        print(results)


def mark_bill_as_paid():
    mycursor = mydb.cursor()
    query = "UPDATE bills SET bill_paid = 'YES' WHERE bill_id=%s"
    bill_id = input("Enter the bill id of the bill to be marked as paid: ")
    vals = (bill_id,)
    mycursor.execute(query, vals)
    results = mycursor.fetchall()
    for res in results:
        print(results)

if __name__=='__main__':
    connectDatabase(host="localhost", username="root", password="Sneha@12")
    print("Connected")
    create_table_customers()
    create_table_bills()
    create_table_users()
    add_user()
    display_users()
    if login():
        add_customer()
        display_customers()
        generate_bill()
        display_bills()
        mark_bill_as_paid()
        display_bills()
