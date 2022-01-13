import re

import MySQLdb.cursors
from flask import Flask, redirect, render_template, request, session, url_for
from flask_mysqldb import MySQL
import wptools
import wikipedia

app = Flask(__name__)
app.secret_key = "hallo"

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'movies'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

def menu():
    Loggedinstate = {}
    try:
        if session["loggedin"]:
            Loggedinstate["url"] = "/login/logout"
            Loggedinstate["title"] = "Logout"
            Loggedinstate["username"] = session["username"]
        else:
            Loggedinstate["title"] = "Login"
            Loggedinstate["url"] = "/login"
            Loggedinstate["username"] = ""
    except:
        Loggedinstate["title"] = "Login"
        Loggedinstate["url"] = "/login"
        Loggedinstate["username"] = ""
    return Loggedinstate


@app.route('/')
def home():
    cur = mysql.connection.cursor()
    cur.execute('''SELECT movie_id,title,release_date FROM movie''')
    rv = cur.fetchall()
    cur.close()

    movies_list = []
    for x in rv:
        url = 'http://127.0.0.1:5000/content?ContentID='+str(x['movie_id'])
        x['url'] = url
        movies_list.append(x)
    return render_template("index.html", movies=movies_list, Loggedin=menu())


@app.route('/login/register', methods=['GET', 'POST'])
def register():
    # Output message if something goes wrong...
    msg = 'Geben sie Ihre Daten ein'
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            'SELECT * FROM users WHERE username = %s', (username,))
        account = cursor.fetchone()
        # If account exists show error and validation checks
        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not username or not password:
            msg = 'Please fill out the form!'
        else:
            cursor.execute(
                'INSERT INTO users (username, pw_hash) VALUES (%s, %s)', (username, password,))
            mysql.connection.commit()
            msg = 'You have successfully registered!'
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    # Show registration form with message (if any)
    return render_template('register.html', msg=msg, Loggedin=menu())


@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = 'login'
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute(
            'SELECT * FROM users WHERE username=%s AND pw_hash=%s', (username, password))
        account = cur.fetchone()
        # If account exists in accounts table in out database
        if account:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['id'] = account['ID']
            session['username'] = account['username']
        # Redirect to home page
            return redirect(url_for('home'))
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'
    return render_template('login.html', msg=msg, Loggedin=menu())


@app.route('/login/logout')
def logout():
    # Remove session data, this will log the user out
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    # Redirect to login page
    return redirect("/")


@app.route('/content')
def content():
    # Gross und kleinschreibung ignorieren
    ContentID = request.args.get('ContentID')
    cur = mysql.connection.cursor()
    cur.execute(f'''SELECT title,release_date FROM movie WHERE movie_id={ContentID}''')
    rv = cur.fetchone()
    cur.close()
    wiki_title = wikipedia.search(rv['title'])[0]
    wiki = {}
    wiki_page = wptools.page(wiki_title)
    wiki_page.get_restbase('/page/summary/')
    wiki[ 'pic' ] = wiki_page.images('url').pop()['url']
    wiki['desc'] = wiki_page.data['extext']
    return render_template('content.html', movie=rv, wiki=wiki, Loggedin=menu())


if __name__ == '__main__':
    app.run(debug=True)
