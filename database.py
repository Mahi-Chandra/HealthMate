import mysql.connector
mycon=mysql.connector.connect(host="localhost",
                              user="root",
                              password="DsOqOlRS@#$%0410",
                              database="world")
if mycon.is_connected():
    print("sucessfully done")
