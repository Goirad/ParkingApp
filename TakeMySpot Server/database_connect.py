#!/usr/bin/python
import mysql.connector as mariadb

mariadb_connection = mariadb.connect(user='lhern207', password='Fastball99', database='takemyspotdb')
cursor = mariadb_connection.cursor()

#retrieving information
some_name = 'Bob Marley'
cursor.execute("SELECT vehicle FROM accounts WHERE name=%s", (some_name,))

print "Vehicle: ", cursor.vehicle

#for first_name, last_name in cursor:
#    print("First name: {}, Last name: {}").format(first_name,last_name)

#insert information
try:
    cursor.execute("INSERT INTO accounts (ID, name, vehicle) VALUES (%d,%s,%s)", (4, 'Maria Test', 'Lexus ES350'))
except mariadb.Error as error:
    print("Error: {}".format(error))

mariadb_connection.commit()
print "The last inserted id was: ", cursor.lastrowid

mariadb_connection.close()