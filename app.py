from flask import Flask, render_template, g, redirect, url_for, request, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3


app = Flask(__name__)
app.secret_key = "ROR2" 
DATABASE = "data.db"


@app.route("/home")  
def home():
    return render_template("home.html", title = "Home")

'''
@app.route("/pizza/<int:id>")
def pizza(id):
    return render_template("pizza.html", id=id)


@app.route('/all_pizzas')
def all_pizzas():
    conn = sqlite3.connect('pizza.db')
    cur = conn.cursor()
    cur.execute('SELECT * FROM Pizza')
    pizzas = cur.fetchall()
    conn.close()
    return render_template('all_pizzas.html', pizzas = pizzas)


@app.route("/pizza/<int:pizza_id>")
def pizza_detail(pizza_id):
    conn = sqlite3.connect('pizza.db')
    cur = conn.cursor()
    
    cur.execute("SELECT * FROM Pizza WHERE id = ?", (pizza_id,))
    pizza = cur.fetchone()
    
    cur.execute("""
        SELECT Topping.name 
        FROM Topping
        JOIN Pizza_Topping ON Topping.id = Pizza_Topping.tid
        WHERE Pizza_Topping.pid = ?
    """, (pizza_id,))
    toppings = [row[0] for row in cur.fetchall()]
    
    conn.close()
    
    if pizza:
        return render_template("pizza_detail.html", pizza=pizza, toppings=toppings)
    else:
        return "Pizza not found", 404

'''

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row 
    return g.db

@app.route('/items')
def items():
    db = get_db()
    item_list = db.execute('SELECT name, description, media FROM Item').fetchall()
    return render_template('items.html', items=item_list)

@app.route('/survivor')
def characters():
    db = get_db()
    survivor_list = db.execute('SELECT name, stats, media FROM Survivor').fetchall()
    return render_template('survivor.html', survivors=survivor_list)

@app.route('/survivor/<name>')
def survivor_info(name):
    db = get_db()
    survivor = db.execute(
        'SELECT * FROM survivor WHERE LOWER(name) = ?', (name,)
    ).fetchone()
    if survivor is None:
        return render_template('survivornotfound.html'), 404
    return render_template('survivor_info.html', survivor=survivor)

@app.route('/item/<name>')
def item_info(name):
    db = get_db()
    item = db.execute(
        'SELECT * FROM item WHERE LOWER(name) = ?', (name,)
    ).fetchone()
    if item is None:
        return render_template('itemnotfound.html'), 404
    return render_template('item_info.html', item=item)

@app.route("/abilities")
def abilities():
    db = get_db()
    ability_list = db.execute('SELECT name, type, cooldown, media, description FROM Abilities').fetchall()
    return render_template('abilities.html', abilities=ability_list)

@app.route('/abilities/<name>')
def abilities_info(name):
    db = get_db()
    ability = db.execute(
        'SELECT * FROM abilities WHERE LOWER(name) = ?', (name,)
    ).fetchone()
    if ability is None:
        return render_template('abilitiesnotfound.html'), 404
    return render_template('abilities_info.html', ability=ability)

@app.route('/maps')
def maps():
    db = get_db()
    map_list = db.execute('SELECT name, description, media, stage FROM Map').fetchall()
    return render_template('maps.html', maps=map_list)

@app.route('/map/<name>')
def map_info(name):
    db = get_db()
    map = db.execute(
        'SELECT * FROM map WHERE LOWER(name) = ?', (name,)
    ).fetchone()
    if map is None:
        return render_template('mapnotfound.html'), 404
    return render_template('map_info.html', map=map)

'''
@app.route('/bosses')
def bosses():
    db = get_db()
    boss_list = db.execute('SELECT name, health, media FROM Boss').fetchall()
    return render_template('bosses.html', bosses=boss_list)

@app.route('/boss/<name>')
def boss_info(name):
    db = get_db()
    boss = db.execute(
        'SELECT * FROM boss WHERE LOWER(name) = ?', (name,)
    ).fetchone()
    if boss is None:
        return "Boss not found", 404
    return render_template('boss_info.html', boss=boss)
'''
    
@app.route('/login', methods=['GET', 'POST'])
def login():
    db = get_db()
    msg = ""
    if request.method == 'POST':
        login_value = request.form['username']
        password = request.form['password']
        user = db.execute('SELECT * FROM User WHERE username = ? OR email = ?', (login_value, login_value)).fetchone()
        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            msg = "Login successful!"
            return redirect(url_for('home'))
        else:
            msg = "Invalid username or password"
    return render_template('login.html', msg=msg)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    db = get_db()
    msg = ""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form.get('email', '')
        existing = db.execute('SELECT * FROM User WHERE username = ?', (username,)).fetchone()
        existing = db.execute('SELECT * FROM User WHERE email = ?', (email,)).fetchone()
        if existing:
            msg = "Username/Email already exists."
        else:
            hashed = generate_password_hash(password)
            db.execute('INSERT INTO User (username, email, password) VALUES (?, ?, ?)', (username, email, hashed))
            db.commit()
            msg = "Registration successful! Please log in."
            return redirect(url_for('login'))
    return render_template('register.html', msg=msg)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route("/")
def index():
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug = True, port=5000)



