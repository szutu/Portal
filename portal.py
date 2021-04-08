from flask import Flask, render_template, request, redirect, url_for, flash
import database

app = Flask(__name__)



app.config.update(dict(
    SECRET_KEY='bradzosekretnawartosc',
))

#docelowo dane będą w przechowywane w bazie
DANE = [{
    'pytanie': 'Stolica Kaszub, to:',
    'odpowiedzi': ['Gdańsk', 'Kościerzyna', 'Kartuzy'],
    'odpok': 'Kartuzy'},
    {
    'pytanie': 'TAK po kaszubsku to:',
    'odpowiedzi': ['jeee', 'jo', 'wsio'],
    'odpok': 'jo'},
    {
    'pytanie': 'Kaszuby to:',
    'odpowiedzi': ['Najpiękniejszy rejon', 'Brzydki rejon', 'Co to Kaszuby?'],
    'odpok': 'Najpiękniejszy rejon'},
]
USERS =[{
    'id':'1','nazwa':'Jakub98'},
{
    'id':'2','nazwa':'RomekKaszuber'},
{
    'id':'3','nazwa':'Kartuzjanin88'},
{
    'id':'4','nazwa':'ŚlązakSzpieg'},
{
    'id':'5','nazwa':'RomanMitoman'},
{
    'id':'6','nazwa':'BoskiBezTroski76'},

]


@app.route('/')
def main():
    return render_template("stronaPowitalna.html")


@app.route('/User/<userId>')
def user(userId):
    wybrany = USERS[(int(userId)-1)]['nazwa']
    return f'Użytkownik o numerze id: {userId} to: ' + wybrany


@app.route('/Dodaj/<zmienna1>+<zmienna2>')
def dodaj(zmienna1, zmienna2):
    wynik = int(zmienna1)+int(zmienna2)
    return f'wynik dodawania to {wynik}'


@app.route('/WolniKaszubi')
def WolniKaszubi():
    return render_template("stronaPowitalna.html")

@app.route('/listaPodstron')
def ListaPodstron():
    return render_template("listaPodstron.html")

@app.route('/ONas')
def ONas():
    return render_template('oNas.html', zm='Nasz serwis jest wolny od wszystkiego, nie ma śledzenia, nie ma leżenia, nie ma niczego.')


@app.route('/Logowanie', methods=['GET', 'POST'])
def Logowanie():
    if request.method == 'POST':
        _name = request.form['inputName']
        _email = request.form['inputEmail']
        _password = request.form['inputPassword']
        print(_name, _email, _password)
        database.insert_one_row(_name, _email, _password)
    return render_template("logowanie.html")


@app.route('/TestKaszuba', methods=['GET', 'POST'])
def TestKaszuba():

    if request.method == 'POST':
        punkty = 0
        odpowiedzi = request.form

        for pnr, odp in odpowiedzi.items():
            if odp == DANE[int(pnr)]['odpok']:
                punkty += 1
                if punkty == 3: ###test
                    print('zdałes')
        flash('Liczba poprawnych odpowiedzi, to: {0}'.format(punkty))
        return redirect(url_for('TestKaszuba'))
    return render_template('TestKaszuba.html', pytania=DANE)


@app.route('/Wyszukiwarka', methods=['GET', 'POST'])
def Wyszukiwarka():
    if request.method == 'POST':
        id = request.form['id']
        #znaleziony = USERS[(int(id)-1)]['nazwa']
        znaleziony = database.select_where('3',id)
        flash('Użytkownik o numerze id: {0}, to {1}' .format(id, znaleziony))
        return redirect(url_for('Wyszukiwarka'))
    return render_template('wyszukiwarka.html')


if __name__ == '__main__':
    app.run(debug=True)
