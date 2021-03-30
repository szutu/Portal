import mysql.connector

# inicjacja połączenia z bazą
mydb = mysql.connector.connect(host="localhost", user="jakub", passwd="fajerwerki", database="mydatabase")
print(mydb)

# inicjacja kursora po naszej bazie z poziomu Python baza nazywa sie mydb nie 'mydatabase'
mycursor = mydb.cursor()


def create_table():
    # mycursor.execute("CREATE DATABASE mydatabase") #w tym wypadku rzeczy w cudzyslowiu sa kąpilowane
    # mycursor.execute("ALTER TABLE users ADD COLUMN id INT AUTO_INCREMENT PRIMARY KEY")
    mycursor.execute("CREATE TABLE users (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), nick VARCHAR(255))")
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


def insert_one_row():
    # uzupelniania tabeli (jeden wiersz)
    sql = "INSERT INTO users (name, nick) VALUES (%s, %s)"
    val = ("Jan", "Nowax78")
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


def select_where():
    # sql = "SELECT * FROM users WHERE nick ='Andrjuu'"
    sql = "SELECT * FROM users WHERE nick LIKE '%Szu%'"
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    for x in myresult:
        print(x)


def sort_db():
    sql = "SELECT * FROM users ORDER BY nick"
    # sql = "SELECT * FROM customers ORDER BY name DESC" #alternative other order
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

def update_table(new_value, previos_value):
    #tabele trzeba zmieniac w poleceniu na razie
    n_v = new_value
    p_v = previos_value
    sql = "UPDATE users SET nick =%s WHERE nick = %s"
    val = (n_v, p_v)
    mycursor.execute(sql, val)
    print(mycursor.rowcount, "record(s) updated")

#create_table()
#insert_many_rows()
# show_db()
show_table()
# select_from_table()
# select_where()
sort_db()
delete_record()
#delete_table('users')
update_table('JOHNFIVE', 'JohnNr5')
sort_db()
