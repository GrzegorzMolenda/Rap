from flask import Flask, render_template, request
import MySQLdb
import konwersja_daty
from datetime import datetime
from dodajemyListyTupli import dodajemy_listy_tupli
app = Flask(__name__)

sel_date = '2010-01-01'
db = MySQLdb.connect("192.0.0.226", "root", "admin", "raporty", charset='utf8', use_unicode=True)

@app.route('/')
def hello_world():
    return render_template('index.html')
######################  D Z I E Ń     ############################
@app.route('/marza/<selected_date>', methods=['GET'])
def marza_view(selected_date):
    # ten rok
    sel_date = selected_date
    curs2 = db.cursor()
    zapytanie_sql2  = "call sp_nowa_marza('"+ selected_date +"','" + selected_date +"');" 
    curs2.execute(zapytanie_sql2)
    curs1 = db.cursor()
    # poprzedni rok
    zapytanie_sql1  = "call sp_nowa_marza('"+ konwersja_daty.zeszly_rok(selected_date)+"','" + konwersja_daty.zeszly_rok(selected_date) +"');"
    curs1.execute(zapytanie_sql1)
    rv1 = curs1.fetchall()  #starsze
    rv2 = curs2.fetchall()  #nowsze
    data_string1 = konwersja_daty.format_daty_marza(konwersja_daty.zeszly_rok(selected_date))
    data_string2 = konwersja_daty.format_daty_marza(selected_date)

    return render_template('marza.html', lista = dodajemy_listy_tupli(rv1, rv2), dt1 = data_string1, dt2 = data_string2) # pierwszy poprzedni, potem obecny, na koniec różnice
#################################  K U M U L A C J A   #########################################################
@app.route('/marza/kumulacja/<selected_date>', methods=['GET'])
def marza_view_kumulacja(selected_date):
    # ten rok
    curs2 = db.cursor()
    zapytanie_sql2  = "call sp_nowa_marza('"+ konwersja_daty.pierwszy_dzien(selected_date) +"','" + selected_date +"');" 
    curs2.execute(zapytanie_sql2)
    curs1 = db.cursor()
    # poprzedni rok
    zapytanie_sql1  = "call sp_nowa_marza('"+ konwersja_daty.pierwszy_dzien_zeszly_rok(selected_date)+"','" + konwersja_daty.ostatni_dzien_zeszly_rok(selected_date) +"');"
    curs1.execute(zapytanie_sql1)
    rv1 = curs1.fetchall()  #starsze
    rv2 = curs2.fetchall()  #nowsze
    data_string1 = konwersja_daty.format_daty_marza(konwersja_daty.ostatni_dzien_zeszly_rok(selected_date))
    data_string2 = konwersja_daty.format_daty_marza(selected_date)
    return render_template('marza.html', lista = dodajemy_listy_tupli(rv1, rv2), dt1 = data_string1, dt2 = data_string2) # pierwszy poprzedni, potem obecny, na koniec różnice
########################################  L I S T A   D N I   ###########################################################
@app.route('/marza/', methods=['GET'])
def marza_view_total():
    curs = db.cursor()
    zapytanie_sql = "SELECT Data, sum(Marza) FROM raporty.wyniki where Data >='2018-01-01' group by Data;"
    curs.execute(zapytanie_sql)
    return render_template('marza_total.html', rv = curs.fetchall(), dt1 = selected_date, dt2 = konwersja_daty.ostatni_dzien_zeszly_rok(selected_date) )





@app.route('/login', methods=['GET', 'POST'])
def login():
    # Here we use a class of some kind to represent and validate our
    # client-side form data. For example, WTForms is a library that will
    # handle this for us, and we use a custom LoginForm to validate.
    form = LoginForm()
    if form.validate_on_submit():
        # Login and validate the user.
        # user should be an instance of your `User` class
        login_user(user)

        flask.flash('Logged in successfully.')

        next = flask.request.args.get('next')
        # is_safe_url should check if the url is safe for redirects.
        # See http://flask.pocoo.org/snippets/62/ for an example.
        if not is_safe_url(next):
            return flask.abort(400)

        return flask.redirect(next or flask.url_for('index'))
    return flask.render_template('login.html', form=form)


@app.errorhandler(500)
def not_found(error):
    return render_template('error.html'),500