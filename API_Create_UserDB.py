'''
This script will automate the process of creating and populating a database of users. 
This will create a SQLlite database, create tables and populate those tables with users. 
You can add more users and control how many each time to add by adjusting the parameter passed to createNumberOfUsers() function
'''


from re import S
import requests
import json
from json import JSONEncoder
import sqlite3
from sqlite3 import Error
import os

#Databases

dbUser = os.path.realpath('./userDB.db')



# create database connection
def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
    
    return conn

# Create Statement. Execute any SQL create table statment
def db_sqlQuery(conn, sql_query):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(sql_query)
    except Error as e:
        print(e) 

# INSERT statment. Use to create insert statments for USERS
def create_task(conn, task):
    """
    Create a new task
    :param conn:
    :param task:
    :return:
    """

    sql = ''' INSERT INTO users(fname,lname,email,email_domain,username,password)
              VALUES(?,?,?,?,?,?) '''

    cur = conn.cursor()
    cur.execute(sql, task)
    conn.commit()
    return cur.lastrowid


'''
Driving Code is below.. Call Main to create and establish database with tables.
Create Number of Users allows you to control how many users you would like to populate 
the created tables with. It does this by using an API to pull json data from a server
'''
# Create database and tables for new users to be populated into
def main():
    global dbUser
    database = dbUser

    sql_create_users_table = """ CREATE TABLE IF NOT EXISTS users (
                                        id integer PRIMARY KEY,
                                        fname text NOT NULL,
                                        lname text,
                                        email text,
                                        email_domain,
                                        username text,
                                        password text
                                    ); """


    # # create a database connection
    conn = create_connection(database)

    # # create tables
    if conn is not None:
        # create tasks table
        db_sqlQuery(conn, sql_create_users_table)
    else:
        print("Error! cannot create the database connection.")

# Makes multiple API calls based on userAmount
# and creates a certain amount of users from the json from the API.
def createNumberOfUsers(userAmount):
    global dbUser
    database = dbUser
    conn = create_connection(database)
    count = userAmount

    while count:
            #Connect to api to generate response object with fake username information
        api_url = "https://randomuser.me/api/"
        response = requests.get(api_url)

        #create json object using the responses .json method.
        json_response = response.json()
        print(json_response['results'][0]['name'])

        # select database to save to
     

        jr = json_response

        emailfull = jr['results'][0]['email']
        emailname = emailfull.split('@')

      
        fname = jr['results'][0]['name']['first']
        lname = jr['results'][0]['name']['last']
        email = emailname[0]
        email_domain = emailname[1]
        username = jr['results'][0]['login']['username']
        password = jr['results'][0]['login']['password']
        user1 = fname, lname, email, email_domain, username, password


        
       
                                           

                                            
        # insert rows
        if conn is not None:
            # create tasks table
            create_task(conn, user1)
        else:
            print("Error! cannot create the database connection.")

        count -= 1



#Create Database and Tables/Schema
main()

#Leverage API to populate a certain amount of Users into database
createNumberOfUsers(10)
