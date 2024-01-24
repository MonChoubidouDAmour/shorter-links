import random
import sqlite3
from flask import Flask, redirect, render_template, request

app = Flask(__name__, template_folder='templates')
database = 'link_database.db'
def create_table():
    db = sqlite3.connect(database)
    cursor = db.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS links (id INTEGER PRIMARY KEY, longlink TEXT, shortlink TEXT UNIQUE)')
    db.commit()

def random_string(length=6):
    letters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    return ''.join(random.choice(letters) for _ in range(length))

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        longlink = request.form.get('longlink')

        if not longlink:
            return render_template('index.html', error='Please enter a LINK')

        create_table()

        with sqlite3.connect(database) as db:
            cursor = db.cursor()
            cursor.execute('SELECT shortlink FROM links WHERE longlink = ?', (longlink,))
            result = cursor.fetchone()

            if result:
                return render_template('index.html', host=request.host_url, shortlink=result[0])

            shortlink = random_string()
            cursor.execute('INSERT INTO links (longlink, shortlink) VALUES (?, ?)', (longlink, shortlink))
            db.commit()
            return render_template('index.html', host=request.host_url, shortlink=shortlink)

    return render_template('index.html')

@app.route('/<shortlink>')
def redirect_shorturl(shortlink):
    with sqlite3.connect(database) as db:
        cursor = db.cursor()
        cursor.execute('SELECT longlink FROM links WHERE shortlink = ?', (shortlink,))
        result = cursor.fetchone()

        return redirect(result[0]) if result else "LINK does not exist"

if __name__ == "__main__":
    app.run(debug=True)
