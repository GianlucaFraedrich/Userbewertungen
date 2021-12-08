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


@app.route('/login')
def login():
    msg = 'login'
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
    return render_template('login.html')


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
