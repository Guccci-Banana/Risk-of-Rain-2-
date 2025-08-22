from flask import Flask, render_template, g
import sqlite3

app = Flask(__name__)
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
        g.db.row_factory = sqlite3.Row  # access columns by name
    return g.db



@app.route('/items')
def items():
    db = get_db()
    item_list = db.execute('SELECT name, description FROM Item').fetchall()
    return render_template('items.html', items=item_list)

@app.route('/survivor')
def characters():
    db = get_db()
    survivor_list = db.execute('SELECT name, stats FROM Survivor').fetchall()
    return render_template('survivor.html', survivors=survivor_list)

@app.route('/survivor/<name>')
def survivor_info(name):
    db = get_db()
    survivor = db.execute(
        'SELECT * FROM survivor WHERE LOWER(name) = ?', (name,)
    ).fetchone()
    if survivor is None:
        return "Survivor not found", 404
    return render_template('survivor_info.html', survivor=survivor)


if __name__ == "__main__":
    app.run(debug = True, port=5001)

