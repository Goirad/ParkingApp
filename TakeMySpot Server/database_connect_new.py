#!/usr/bin/python3

#PyMySQL depending on distro might have dependencies on either mysqlclient or MySQLdb packages.
#Most likely latest MySQLdb must be installed for PyMySQL to work.
import pymysql

# Open database connection
db = pymysql.connect("localhost","root","Fastball99","takemyspotdb" )

# prepare a cursor object using cursor() method
cursor = db.cursor()

# execute SQL query using execute() method.
#The killer was driving a Suzuki Minivan
cursor.execute("SELECT Name FROM accounts WHERE vehicle = 'Suzuki Minivan'")

# Fetch a single row using fetchone() method.
data = cursor.fetchone()

print ("Name of the killer : %s " % data)

# disconnect from server
db.close()
