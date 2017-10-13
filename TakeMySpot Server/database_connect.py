#!/usr/bin/python
import mysql.connector as mariadb

mariadb_connection = mariadb.connect( user='root', password='Fastball99', database='takemyspotdb')
cursor = mariadb_connection.cursor()

#retrieving information
some_name = 'Bob Marley'

try:
    cursor.execute("SELECT Vehicle, ID FROM accounts WHERE Name=%s", (some_name,))
except mariadb.Error as error:
    print("Error: {}".format(error))


for Vehicle, ID in cursor:
    print("Vehicle: {}, ID: {}").format(Vehicle,ID)

#insert information
try:
    cursor.execute("INSERT INTO accounts (Name, Vehicle) VALUES (%s,%s)", ('Maria Test', 'Lexus ES350'))
except mariadb.Error as error:
    print("Error: {}".format(error))

mariadb_connection.commit()
print ("The last inserted id was: ", cursor.lastrowid)

mariadb_connection.close()
