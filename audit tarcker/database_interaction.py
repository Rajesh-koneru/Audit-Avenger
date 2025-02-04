from flask import Flask ,jsonify
from flask_sqlalchemy import SQLAlchemy
import sqlite3
audit=Flask(__name__)
audit.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///auditTracker.db'  # SQLite for simplicity
audit.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable modification tracking for performance

# list the tables in the data base
def tables_info():
    conn = sqlite3.connect('auditTracker.db')
    pointer = conn.cursor()
    try:
        sqlfetch = ''' SELECT name FROM sqlite_master WHERE type="table";'''
        pointer.execute(sqlfetch)
        data = pointer.fetchall()
        list1=[]
        for data in data:
            list1.append(data)
            print(data)
        return list1
    except sqlite3.OperationalError as e:
        print(e)
    finally:
        conn.close()

tab_name=tables_info()
print(tab_name)

# create a new table
def create_table(user,column_name):
    conn = sqlite3.connect('auditTracker.db')
    pointer = conn.cursor()
    try:
        #create table user
            sql1 = f'''
            CREATE TABLE  {user} ({column_name});
            '''
            pointer.execute(sql1)
            print (f'table created ')

    except sqlite3.OperationalError as e:
        print(e)
        return create_table


# data inserting
def insertdata(passwrd,inpt):
    conn = sqlite3.connect('auditTracker.db')
    pointer = conn.cursor()
    try:
        sql3 =f''' 
    insert into {passwrd}  values ({inpt});'''
        pointer.execute(sql3)
        print('data inserted')
        return insertdata
    except sqlite3.OperationalError as e:
        print(e)
    finally:
        conn.commit()
        conn.close()


# show information in the tables data


def show_data_from_table(passw):
    # Function to display data from the table
    conn = sqlite3.connect('auditTracker.db')
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {passw} ;")
    rows = cursor.fetchall()
    for row in rows:
        print(row)
    return rows

# drop table
def drop_table(table):
    conn = sqlite3.connect('auditTracker.db')
    pointer = conn.cursor()
    try:
        sql_drop=f'''drop table {table}'''
        pointer.execute(sql_drop)
        print('delited')
    except sqlite3.OperationalError as e:
        print(e)
    finally:
        conn.commit()
        conn.close()
def column(table_name):
    conn = sqlite3.connect('auditTracker.db')
    pointer = conn.cursor()

    try:
         value = table_name
         sql1 = f"PRAGMA table_info('{value}');"
         print(value)
         pointer.execute(sql1)
         data = pointer.fetchall()
         count = 0
         for colum in data:
             print(f"Column Name: {colum[1]}, Data Type: {colum[2]}")
             count += 1
         print(count)
    except sqlite3.OperationalError as e:
        print(e)
    return column
def main():
    n=int(input('enter number '))
    if n==1:
        table_name = input('enter table name:')
        # Initialize an empty list to store column definitions
        columns = []

        # Example of getting multiple columns from the user
        while True:
            column_input = input("Enter column name and type (or type 'done' to finish): ")

            if column_input.lower() == 'done':
                break  # Exit the loop when user types 'done'
            columns.append(column_input)  # Add the column definition to the list
        # Now, columns contains all the user inputs
        print("Columns to be added:", columns)

        # Example of how to use the columns list in a CREATE TABLE statement
        columns_input = ', '.join(columns)  # Combine all column definitions into a single string
        create_table(table_name, columns_input)
    elif n==2:
       colum=[]
       table=input('enter the table name ')
       value = input('enter the values')
       print(value)
       colum.append(value)
       print(colum)
       columns_input = ', '.join(colum)
       insertdata(table,columns_input)
    elif n==3:
        table = input('enter the table name for data retrival ')
        show_data_from_table(table)
    elif n==4:
        drop=input('enter the table name for table delete ')
        drop_table(drop)
    elif n==5:
        table_name=input('enter the table name')
        column(table_name)
    else:
        print('enter a valid number')
main()







