import mysql.connector
mydb = mysql.connector.connect(host="localhost", user="jakub", passwd="fajerwerki")
# inicjacja połączenia z bazą
print(mydb)

if(mydb):
    print('Kontakt z bazą')
else:
    print('Nie ma kontaktu z baza')