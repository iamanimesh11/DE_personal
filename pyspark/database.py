import mysql.connector
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="@Nimesh11"
)

mycursor = mydb.cursor()

mycursor.execute("CREATE table trialmydatabase.x ( a varchar(255))")

print(mydb)


