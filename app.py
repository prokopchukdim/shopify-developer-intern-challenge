from datetime import datetime
from flask import Flask, render_template, url_for, flash, redirect, request
from flask_sqlalchemy import SQLAlchemy

#Initialization
app = Flask(__name__, template_folder = "templates")
app.config['SECRET_KEY'] = 'demo_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.db'
db = SQLAlchemy(app)

#Relation for inventory items
class Inventory(db.Model):
    __tablename__ = "Inventory"
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    warehouseid = db.Column(db.Integer)
    name = db.Column(db.String(100))
    quantity = db.Column(db.Integer)

    #Return a string representation of a row in the relation
    def __repr__(self):
        return f"Inventory('{self.id}','{self.name}','{self.warehouseid}', '{self.quantity}')"

#Relation for warehouses
class Warehouse(db.Model):
    __tablename__ = "Warehouse"
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.String(100))
    address = db.Column(db.String(200))

    #Return a string representation of a row in the relation
    def __repr__(self):
        return f"Warehouse('{self.id}', '{self.name}', '{self.address}')"

@app.route('/')
@app.route('/home')
@app.route('/inventory', methods = ['GET', 'POST'])
def home():
    if request.method == 'POST':
        #Update Inventory relation

        #Parse input
        name = request.form['name']
        warehouse = request.form['warehouse']
        quantity = request.form['quantity']

        #update warehouse to point to warehouse id
        warehouse = int(warehouse[0:warehouse.find(":")])

        #Different items can potentially have the same name, so no checking for duplicate inventory.

        item = Inventory(name = name, warehouseid = warehouse, quantity = quantity)
        db.session.add(item)
        db.session.commit()

        return redirect(url_for("home"))
    
    else:
        #Redirect user to home page
        inventory = db.engine.execute("SELECT * FROM inventory").all()
        wh = db.engine.execute("SELECT * FROM warehouse").all()
        return render_template("index.html", inventory=inventory, wh = wh)

@app.route('/warehouses')
def warehouses():
    inventory = db.engine.execute("SELECT * FROM inventory").all()
    wh = db.engine.execute("SELECT * FROM warehouse").all()
    return render_template("index.html", inventory = inventory, wh = wh)

@app.route('/delete', methods = ['POST'])
def delete():
    id = request.form["id"]
    db.engine.execute("DELETE FROM inventory WHERE id = :id", {"id":id})
    return redirect(url_for("home"))

@app.route('/update-inv', methods = ['POST'])
def updateinv():
    id = request.form["id"]
    warehouse = request.form['wh']
    warehouse = int(warehouse[0:warehouse.find(":")])
    quantity = request.form['quantity']
    name = request.form['name']
    print(id + str(warehouse) +quantity + name)

    db.engine.execute("UPDATE inventory SET warehouseid = :wh, quantity = :q, name = :name WHERE id = :id", {"wh":warehouse, "q":quantity, "name": name, "id":id})
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug = True)