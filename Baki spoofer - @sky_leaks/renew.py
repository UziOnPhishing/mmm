import mysql.connector

bdd = mysql.connector.connect(host="localhost",user="zystew",password="2w6Txj9PH", database="baki")

cursor = bdd.cursor()
cursor.execute("UPDATE clients set max=500")
bdd.commit()

bdd.close()