from flask import Flask, render_template, request
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'Userratings'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)


@app.route('/')
def home():
    cur = mysql.connection.cursor()
    cur.execute('''SELECT * FROM content''')
    rv = cur.fetchall()
    cur.close()

    movies_list = []
    for x in rv:
        url = 'http://127.0.0.1:5000/content?ContentID='+str(x['id'])
        x['url'] = url
        movies_list.append(x)

    return render_template("index.html", movies=movies_list)


@app.route('/login/register', methods=['GET', 'POST'])
def register():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    # Show registration form with message (if any)
    return render_template('register.html', msg=msg)


@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = 'login'
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']

    cur = mysql.connection.cursor()
    cur.execute(
        f'''SELECT * FROM our_users WHERE Nickname={username} AND pw_hash={password}''')
    account = cur.fetchone()
    # If account exists in accounts table in out database
    if account:
        # Create session data, we can access this data in other routes
        session['loggedin'] = True
        session['id'] = account['id']
        session['username'] = account['username']
        # Redirect to home page
        return 'Logged in successfully!'
    else:
        # Account doesnt exist or username/password incorrect
        msg = 'Incorrect username/password!'
    return render_template('login.html', msg=msg)


@app.route('/login/logout')
def logout():
    # Remove session data, this will log the user out
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    # Redirect to login page
    return redirect(url_for('login'))


@app.route('/content')
def content():
    # Gross und kleinschreibung ignorieren
    ContentID = request.args.get('ContentID')
    cur = mysql.connection.cursor()
    cur.execute(f'''SELECT * FROM content WHERE id={ContentID}''')
    rv = cur.fetchone()
    cur.close()
    return render_template('content.html', movie=rv)


if __name__ == '__main__':
    app.run(debug=True)
