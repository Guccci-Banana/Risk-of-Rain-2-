# Importing necessary libraries
from flask import (
    Flask, render_template, g, redirect, url_for, request, session
)
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3


# Initialize flask and connecting to database
app = Flask(__name__)
app.secret_key = "ROR2"
DATABASE = "data.db"


# Default route
@app.route("/")
def index():
    return redirect(url_for("home"))


# Home route
@app.route("/home")
def home():
    loggedin = session.get('loggedin', 'no')
    return render_template("home.html", title="Home", loggedin=loggedin)


# Database connection
def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
    return g.db


# Items page route
@app.route('/items')
def items():
    db = get_db()
    item_list = db.execute(
        'SELECT name, description, media, stack_type, dlc, rarity FROM Item'
    ).fetchall()
    return render_template('items.html', items=item_list)


# Characters page route
@app.route('/survivor')
def characters():
    db = get_db()
    survivor_list = db.execute('SELECT * FROM Survivor').fetchall()
    return render_template('survivor.html', survivors=survivor_list)


# Indiviual survivor page route
@app.route('/survivor/<name>')
def survivor_info(name):
    db = get_db()
    survivor = db.execute(
        'SELECT * FROM survivor WHERE LOWER(name) = ?', (name,)
    ).fetchone()
    if survivor is None:
        return render_template('survivornotfound.html'), 404
    return render_template('survivor_info.html', survivor=survivor)


# Individual item page route
@app.route('/item/<name>')
def item_info(name):
    db = get_db()
    item = db.execute(
        'SELECT * FROM item WHERE LOWER(name) = ?', (name,)
    ).fetchone()
    if item is None:
        return render_template('itemnotfound.html'), 404
    return render_template('item_info.html', item=item)


# Abilities page route
@app.route("/abilities")
def abilities():
    db = get_db()
    ability_list = db.execute(
        'SELECT name, type, cooldown, media, description FROM Abilities'
    ).fetchall()
    return render_template('abilities.html', abilities=ability_list)


# Individual ability page route
@app.route('/abilities/<name>')
def abilities_info(name):
    db = get_db()
    ability = db.execute(
        'SELECT * FROM abilities WHERE LOWER(name) = ?', (name,)
    ).fetchone()
    if ability is None:
        return render_template('abilitiesnotfound.html'), 404
    return render_template('abilities_info.html', ability=ability)


# Maps page route
@app.route('/maps')
def maps():
    db = get_db()
    map_list = db.execute(
        'SELECT name, description, media, stage FROM Map'
    ).fetchall()
    return render_template('maps.html', maps=map_list)


# Individual map page route
@app.route('/map/<name>')
def map_info(name):
    db = get_db()
    map = db.execute(
        'SELECT * FROM map WHERE LOWER(name) = ?', (name,)
    ).fetchone()
    if map is None:
        return render_template('mapnotfound.html'), 404
    bosses = db.execute(
        'SELECT b.name '
        'FROM Boss b '
        'JOIN BossMap bm ON b.id = bm.boss_id '
        'JOIN Map m ON bm.map_id = m.id '
        'WHERE LOWER(m.name) = ?',
        (name,)
    ).fetchall()
    return render_template('map_info.html', map=map, bosses=bosses)


# Individual survivor Stories page route
@app.route('/survivorstory/<name>')
def survivorstory(name):
    db = get_db()
    survivor = db.execute(
        'SELECT * FROM survivor WHERE LOWER(name) = ?', (name,)
    ).fetchone()
    if survivor is None:
        return render_template('survivornotfound.html'), 404
    return render_template('survivorstory.html', survivor=survivor)


# Bosses page route
@app.route('/bosses')
def bosses():
    db = get_db()
    boss_list = db.execute('SELECT name, health, media FROM Boss').fetchall()
    return render_template('bosses.html', bosses=boss_list)


# Individual boss page route
@app.route('/boss/<name>')
def boss_info(name):
    db = get_db()
    boss = db.execute(
        'SELECT * FROM boss WHERE LOWER(name) = ?', (name,)
    ).fetchone()
    if boss is None:
        return render_template('bossnotfound.html'), 404
    maps = db.execute(
        'SELECT m.name FROM Map m '
        'JOIN BossMap bm ON m.id = bm.map_id '
        'JOIN Boss b ON bm.boss_id = b.id '
        'WHERE LOWER(b.name) = ?',
        (name,)
    ).fetchall()
    return render_template('boss_info.html', boss=boss, maps=maps)


# User login code and route
@app.route('/login', methods=['GET', 'POST'])
def login():
    db = get_db()
    msg = ""
    if request.method == 'POST':
        login_value = request.form['username']
        password = request.form['password']
        user = db.execute(
            'SELECT * FROM User WHERE username = ? OR email = ?',
            (login_value, login_value)
        ).fetchone()
        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            msg = "Login successful!"
            session["loggedin"] = "yes"
            return redirect(url_for('home'))
        else:
            msg = "Invalid username or password"
    return render_template('login.html', msg=msg)


# User logout route
@app.route('/logout')
def logout():
    session["loggedin"] = "no"
    session.clear()
    return redirect(url_for('login'))


# User registration code and route
@app.route('/register', methods=['GET', 'POST'])
def register():
    db = get_db()
    msg = ""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form.get('email', '')
        existing = db.execute(
            'SELECT * FROM User WHERE username = ?', (username,)
        ).fetchone()
        existing = db.execute(
            'SELECT * FROM User WHERE email = ?', (email,)
        ).fetchone()
        if existing:
            msg = "Username/Email already exists."
        else:
            hashed = generate_password_hash(password)
            db.execute(
                ('INSERT INTO User (username, email, password)'
                 'VALUES (?, ?, ?)'),
                (username, email, hashed)
            )
            db.commit()
            msg = "Registration successful! Please log in."
            return redirect(url_for('login'))
    return render_template('register.html', msg=msg)


# Search function route
@app.route('/search', methods=['GET', 'POST'])
def search():
    db = get_db()
    results = []
    query = ""
    if request.method == 'POST':
        query = request.form['query'].lower()
        item_results = db.execute(
            'SELECT * FROM Item '
            'WHERE LOWER(name) LIKE ?', (
                '%' + query + '%',
            )
        ).fetchall()
        survivor_results = db.execute(
            'SELECT * FROM Survivor '
            'WHERE LOWER(name) LIKE ?', (
                '%' + query + '%',
                )
            ).fetchall()
        ability_results = db.execute(
            'SELECT * FROM Abilities '
            'WHERE LOWER(name) LIKE ?'
            'OR LOWER(traits) LIKE ?', (
                '%' + query + '%', '%' + query + '%'
                )
            ).fetchall()
        map_results = db.execute(
            'SELECT * FROM Map '
            'WHERE LOWER(name) LIKE ?', (
                '%' + query + '%',
                )
            ).fetchall()
        boss_results = db.execute(
            'SELECT * FROM Boss '
            'WHERE LOWER(name) LIKE ?', (
                '%' + query + '%',
                )
            ).fetchall()
        results = {
            'items': item_results,
            'survivors': survivor_results,
            'abilities': ability_results,
            'maps': map_results,
            'boss': boss_results
        }
    return render_template('search.html', results=results, query=query)


# Page not founderror handling route
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


# Running the app
if __name__ == "__main__":
    app.run(debug=True, port=5000)
