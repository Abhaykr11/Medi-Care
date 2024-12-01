import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password='root',
    port=3306,
    database='hbill'
)
mycursor = mydb.cursor()

mycursor.execute("select * from admin")

admin = mycursor.fetchall()

for user in admin:
    print(user)
    print('username ' + user[1])
    print('password ' + user[2])
