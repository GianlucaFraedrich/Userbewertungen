from flask import Flask, render_template
from flask_pymysql import MySQL


app = Flask(__name__)

# This example assumes a valid username and password are in the client section of a ~/.my.cnf file.
# This is a well known standard for mysql/mariadb clients.
# Example contents of ~/.my.cnf :
# [client]
# user = my_user_name
# password = super_secret_password
# This means your password is now not stored with your code!

connect_args = {'read_default_file': '~/.my.cnf',
                'autocommit': True,
                'cursorclass': 'DictCursor',
                'user': 'root',
                'password': '',
                'host': '127.0.0.1',
                'db': 'Userratings'
                }

mysql = MySQL(app.app_context())

conn = mysql.connect(cursorclass='DictCursor')
cursor = conn.cursor()


@app.route('/')
def users():
    cursor.execute('''SELECT * FROM content''')
    rv = cursor.fetchall()
    print(rv)
    return render_template("index.html", movies=rv)


if __name__ == '__main__':
    app.run(debug=True)
