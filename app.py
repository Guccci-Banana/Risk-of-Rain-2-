from flask import Flask, render_template
import sqlite3

app = Flask(__name__)


@app.route("/")  
def home():
    return render_template("home.html", title = "Home")


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
    


if __name__ == "__main__":
    app.run(debug = True)
