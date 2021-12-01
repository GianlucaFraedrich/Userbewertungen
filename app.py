from flask import Flask, render_template
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'Userratings'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)


@app.route('/')
def users():
    cur = mysql.connection.cursor()
    cur.execute('''SELECT * FROM content''')
    rv = cur.fetchall()
    cur.close()
    print(rv)
    return render_template("index.html", movies=rv)


if __name__ == '__main__':
    app.run(debug=True)
