import mysql.connector
import re

# inicjacja połączenia z bazą
mydb = mysql.connector.connect(host="localhost", user="jakub", passwd="fajerwerki", database="mydatabase")
print(mydb)

# inicjacja kursora po naszej bazie z poziomu Python baza nazywa sie mydb nie 'mydatabase'
mycursor = mydb.cursor()


def create_table(table_name):
    # mycursor.execute("CREATE DATABASE mydatabase") #w tym wypadku rzeczy w cudzyslowiu sa kąpilowane
    # mycursor.execute("ALTER TABLE users ADD COLUMN id INT AUTO_INCREMENT PRIMARY KEY")
    mycursor.execute("CREATE TABLE {0} (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), email VARCHAR(255), password VARCHAR(255))" .format(table_name))
    # powyzsze są zakomitowane bo raz wykonane są już zapisane!!, możliwe ze to sie powinno gdzie indziej pisac


def show_db():
    # wyswietlenie zawartosci bazy
    mycursor.execute("SHOW DATABASES")
    for x in mycursor:
        print(x)


def show_table():
    mycursor.execute("SHOW TABLES")
    for x in mycursor:
        print(x)


# sprawdzenie czy jest kontakt z bazą
def check_connection():
    if (mydb):
        print('Kontakt z bazą')
    else:
        print('Nie ma kontaktu z baza')


def insert_one_row(arg1, arg2, arg3):
    # uzupelniania tabeli (jeden wiersz)
    #sql = "INSERT INTO users (name, nick) VALUES (%s, %s, )"
    sql = "INSERT INTO dane (name, email, password) VALUES (%s, %s, %s)"
    val = (arg1, arg2, arg3)
    mycursor.execute(sql, val)
    mydb.commit()  # ten commit jest wymagany aby dokonac zmian w bazie
    print(mycursor.rowcount, "record inserted.")


# uzupelnienie tabeli (wiele wierszy)
def insert_many_rows():
    sql = "INSERT INTO users (name, nick) VALUES (%s, %s)"
    val = [  # tutaj mamy listę krotek, aby mozna za jednym razem wstawic wiele
        ('Roman', 'romekAtomek'),
        ('Andrzej', 'Andrjuu'),
        ('Monika', 'DziewczynaRatownika88'),
        ('Jan', 'JohnNr5'),
        ('Beata', 'Betrixy'),
    ]
    mycursor.executemany(sql, val)  # tutaj dopisek 'many' wskazuje na uzupelnienie WIELU wierszy na raz
    mydb.commit()  # wymagane aby dokonac zmian w bazie
    print(mycursor.rowcount, "was inserted.")
    print("1 record inserted, ID:", mycursor.lastrowid)  # kazde odpalenie dodaje kolejne rekordy


def select_from_table():
    # mycursor.execute("SELECT * FROM users")
    mycursor.execute("SELECT name FROM users")  # wybrane kolumny tylko
    myresult = mycursor.fetchall()
    # myresult = mycursor.fetchone() #zwraca pierwszy wiersz z select
    for x in myresult:
        print(x)


def select_where(choice, search):
    if choice == '1':
        sql = ("SELECT * FROM users WHERE nick ='%s'" % search)
    elif choice == '2':
        sql = ("SELECT * FROM users WHERE nick LIKE '%{0}%'" .format(search))
    else:
        sql = ("SELECT * FROM dane WHERE id LIKE '%{0}%'" .format(search))
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    for x in myresult:
        print(x)
    return myresult


def sort_db(choice1, choice2):
    if choice1 == "nick":
        sql = "SELECT * FROM users ORDER BY nick "
    elif choice1 == "name":
        sql = "SELECT * FROM users ORDER BY name "
    elif choice1 == "id":
        sql = "SELECT * FROM users ORDER BY id "
    if choice2 == "asc" or choice2 == "ASC":
        sql += "ASC" #alternative other order
    else:
        sql += "DESC"
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    for x in myresult:
        print(x)


def delete_record():
    sql = "DELETE FROM users WHERE nick ='Andrjuu'"  # string 'sql' to polecenie SQL
    mycursor.execute(sql)  # tutaj 'wysylamy' polecenie SQL do kursora iterujacego po bazie
    mydb.commit()  # konieczne zeby dokonac zmian w bazie tj. dodawanie usuwanie itp
    print(mycursor.rowcount, "record(s) deleted")


def delete_table(table):
    sql = "DROP TABLE IF EXISTS "
    sql += table
    mycursor.execute(sql)

def update_table(what_to_change, previos_value, new_value):
    #tabele trzeba zmieniac w poleceniu na razie
    if what_to_change == "nick":
        sql = "UPDATE users SET nick =%s WHERE nick = %s"
    elif what_to_change == "name":
        sql = "UPDATE users SET name =%s WHERE name = %s"
    val = (new_value, previos_value)
    mycursor.execute(sql, val)
    print(mycursor.rowcount, "record(s) updated")

#create_table(input("Podaj nazwę tabeli która chcesz utworzyć: "))
#insert_many_rows()
# show_db()
#show_table()
# select_from_table()
#select_where(input("Jeżeli chcesz wyszukać po całym nicku wpisz: 1\nJeżeli po jego części wpisz: 2\n"), input("Wpisz szukaną fraze: "))
#sort_db((input("Jeśli chcesz posotrować po nickach wpisz: 'nick', jeśli po imionach wpisz 'name', jeśli id to 'id' ")), (input("jesli chcesz posortować rosnąca wpisz: 'asc', jeśli malejąco wpisz cokolwiek ")))
#delete_record()
#delete_table('users')
#update_table((input("podaj która kolumne chcesz zastąpić, wpisz 'nick' lub 'name'")), (input("podaj którą wartość chcesz zastąpić")), (input("podaj nową wartość: ")))
#sort_db()
#insert_one_row(input("podaj nazwę tabeli, którą chcesz uzupełnić: "), (input("podaj imie: ")), (input("podaj email: "), input("Podaj haslo")))
