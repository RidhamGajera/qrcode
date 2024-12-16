from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import qrcode

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class MenuItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Float, nullable=False)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    menu_item_id = db.Column(db.Integer, db.ForeignKey('menu_item.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

@app.route('/')
def menu():
    menu_items = MenuItem.query.all()
    return render_template('menu.html', menu_items=menu_items)

@app.route('/order', methods=['POST'])
def order():
    menu_item_id = request.form['menu_item_id']
    quantity = int(request.form['quantity'])
    new_order = Order(menu_item_id=menu_item_id, quantity=quantity)
    db.session.add(new_order)
    db.session.commit()
    return redirect(url_for('menu'))

@app.route('/admin')
def admin():
    menu_items = MenuItem.query.all()
    orders = Order.query.all()
    return render_template('admin.html', menu_items=menu_items, orders=orders)

@app.route('/add_menu', methods=['POST'])
def add_menu_item():
    name = request.form['name']
    description = request.form['description']
    price = request.form['price']
    new_item = MenuItem(name=name, description=description, price=price)
    db.session.add(new_item)
    db.session.commit()
    return redirect(url_for('admin'))

@app.route('/generate_qr')
def generate_qr():
    qr = qrcode.make(request.host_url)
    qr.save('static/qr_code.png')
    return redirect(url_for('admin'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
