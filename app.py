from flask import Flask, render_template, request, session, url_for, redirect
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re

app = Flask(__name__)
app.secret_key = "hallo"

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'Userratings'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)


def menu():
    Loggedinstate = {}
    try:
        if session["loggedin"]:
            Loggedinstate["url"] = "/login/logout"
            Loggedinstate["title"] = "Logout"
            Loggedinstate["username"] = session["username"]
            if(session['admin'] == b'\x01'):
                Loggedinstate['admin'] = True
            else:
                Loggedinstate['admin'] = False
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
    # Get Parameters
    searchtext = request.args.get('search')
    add_sql = ''

    # Get existing genres
    cur = mysql.connection.cursor()
    cur.execute('''SELECT * FROM genre''')
    genres = cur.fetchall()
    cur.close()

    # Check parameters for genres
    matching_genres_ids = []
    for genre in genres:
        genre_name = genre['genre']
        x = request.args.get(genre_name)
        if(x == "True"):
            matching_genres_ids.append(genre['ID'])
    # Search

    cur = mysql.connection.cursor()
    if((searchtext == None) & (matching_genres_ids == [])):
        cur.execute('''SELECT * FROM content''')
    else:
        if(matching_genres_ids != []):
            add_sql = ' AND content_genre.contentID=content.ID AND genre.ID=content_genre.genreID'
            for matching_genre_id in matching_genres_ids:
                add_sql += f' AND genre.ID={matching_genre_id}'
        cur.execute(
            f'''SELECT DISTINCT content.Titel, content.ID, content.release_date FROM content, genre, content_genre WHERE content.Titel LIKE \'{searchtext}%\'{add_sql}''')
    rv = cur.fetchall()
    cur.close()

    # Create Content Table
    movies_list = []
    for x in rv:
        url = 'http://127.0.0.1:5000/content?ContentID='+str(x['ID'])
        x['url'] = url
        url = 'http://127.0.0.1:5000/content/delete?ContentID='+str(x['ID'])
        x['del_url'] = url
        movies_list.append(x)

    # Merken der angecheckten Boxen und wieder neu markieren
    new_genre = []
    if(matching_genres_ids != []):
        for genre in genres:
            genre['state'] = ""
            for matching_genre_id in matching_genres_ids:
                if(genre['ID'] == matching_genre_id):
                    genre['state'] = "checked"  # Space is important
            new_genre.append(genre)
        genres = tuple(new_genre)

    return render_template("index.html", movies=movies_list, genres=genres, Loggedin=menu())


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
            session['admin'] = account['admin_flag']
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
    session.pop('admin', None)
    # Redirect to login page
    return redirect("/")


@app.route('/content')
def content():
    ContentID = request.args.get('ContentID')
    cur = mysql.connection.cursor()
    cur.execute(f'''SELECT * FROM content WHERE id={ContentID}''')
    rv = cur.fetchone()
    cur.close()
    if(session.get('admin') == b'\x01'):
        # Get existing genres
        cur = mysql.connection.cursor()
        cur.execute('''SELECT * FROM genre''')
        genres = cur.fetchall()
        cur.close()
        return render_template('content_admin.html', genres=genres, movie=rv, Loggedin=menu())
    else:
        # Just get the Genres to the specific movie
        cur = mysql.connection.cursor()
        cur.execute(
            f'''SELECT * FROM genre, content_genre WHERE contentID={ContentID} AND genreID=genre.ID''')
        genres = cur.fetchall()
        cur.close()
        return render_template('content.html', movie=rv, genres=genres, Loggedin=menu())


@app.route('/content/delete')
def delete():
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    try:
        ContentID = int(request.args.get('ContentID'))
        if(session.get('admin') == b'\x01'):
            cur = mysql.connection.cursor()
            cur.execute(f'''DELETE FROM content WHERE id={ContentID}''')
            cur.close()
        else:
            return "403"
        return redirect("/")
    except:
        return "...Fehlerbehandlung?"


if __name__ == '__main__':
    app.run(debug=True)
