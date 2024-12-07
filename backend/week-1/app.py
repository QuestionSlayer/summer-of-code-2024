from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy.orm import validates
import json
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)


class InventoryItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Item_SKU = db.Column(db.String(20), unique=False, nullable=False, index=True)
    Item_Name = db.Column(db.String(20), unique=False, nullable=False)
    Item_Description = db.Column(db.String(50), unique=False, nullable=True)
    Item_Price = db.Column(db.Integer, nullable=False)
    Item_Qty = db.Column(db.Integer, nullable=False)
    @validates('Item_Price','Item_Qty')
    def validate_price(self,key,value):
        if value<0:
            raise ValueError(f'{key} cannot be negative')
        return value

    def __repr__(self):
        return f"Name: {self.Item_Name}, Price: {self.Item_Price}, Qty: {self.Item_Qty}"


class Customer(db.Model):
    c_ID = db.Column(db.Integer, primary_key=True)
    c_name = db.Column(db.String(20), unique=False, nullable=False)
    c_email = db.Column(db.String(50), unique=True, nullable=False, index=True)
    c_contact = db.Column(db.String(15), unique=True, nullable=False)
    @validates('c_email')
    def validate_email(self,key,value):
        if ('@'or '.') not in value:
            raise ValueError('Invalid Email')
        return value
    def __repr__(self):
        return f"Customer: {self.c_name}, Email: {self.c_email}"


class Staff(db.Model):
    s_ID = db.Column(db.Integer, primary_key=True)
    s_name = db.Column(db.String(20), unique=False, nullable=False)
    s_email = db.Column(db.String(50), unique=True, nullable=False)
    s_isAdmin = db.Column(db.Boolean, nullable=False)
    s_contact = db.Column(db.String(15), unique=True, nullable=False)

    def __repr__(self):
        return f"Staff: {self.s_name}, Is Admin: {self.s_isAdmin}"


class Transaction(db.Model):
    t_ID = db.Column(db.Integer, primary_key=True)
    c_ID = db.Column(db.Integer, db.ForeignKey('customer.c_ID'), nullable=False) 
    s_ID = db.Column(db.Integer, db.ForeignKey('staff.s_ID'), nullable=False)    
    Item_ID = db.Column(db.Integer, db.ForeignKey('inventory_item.Item_SKU'), nullable=False)  
    t_date = db.Column(db.DateTime, default=datetime.now, nullable=False)
    t_amount = db.Column(db.Integer, nullable=False)
    t_category = db.Column(db.String(20), unique=False, nullable=False)

    def __repr__(self):
        return f"Transaction ID: {self.t_ID}, Amount: {self.t_amount}, Date: {self.t_date}"
def fill_items(json_file):
    with open(json_file,'r') as seed_item:
        data=json.load(seed_item)
        for i in data:
            item=InventoryItem(
                Item_SKU= i['SKU'],
                Item_Name=i['Name'],
                Item_Price=i['Price'],
                Item_Qty=i['Quantity'],
                Item_Description=i['Description']
            )
            db.session.add(item)
        db.session.commit()
        print("Items added to database succesfully")
def fill_customers(json_file):
    with open(json_file,'r') as seed_customer:
        data=json.load(seed_customer)
        for i in data:
            new_customer=Customer(
                c_name= i['Name'],
                c_email=i['Email'],
                c_contact=i['Contact']
            )
            db.session.add(new_customer)
        db.session.commit()
        print("Customer added to database succesfully")
def fill_staff(json_file):
    with open(json_file,'r') as seed_staff:
        data=json.load(seed_staff)
        for i in data:
            new_staff=Staff(
                s_name= i['Name'],
                s_email=i['Email'],
                s_contact=i['Contact'],
                s_isAdmin=i['Admin']
            )
            db.session.add(new_staff)
        db.session.commit()
        print("Staff added to database succesfully")
def fill_txn(json_file):
    with open(json_file,'r') as seed_txn:
        data=json.load(seed_txn)
        for i in data:
            new_txn=Transaction(
                s_ID=i['Staff'],
                c_ID=i['Customer'],
                Item_ID=i['SKU'],
                t_amount=i['Amount'],
                t_category=i['Category']
            )
            db.session.add(new_txn)
        db.session.commit()
        print("Transaction added to database succesfully")
with app.app_context():
    db.create_all()


@app.route("/")
def home():
    return "Flask App Connected to Database Successfully!"

# Route to Add Sample Data
@app.route("/add_customer")
def add_customer():
    fill_customers("C:\\Users\\lenovo\\Documents\\DSOC\\winter24\\seeds\\customers.json")
    return "Customers added succesfully"
@app.route("/add_staff")
def add_staff():
    fill_staff("C:\\Users\\lenovo\\Documents\\DSOC\\winter24\\seeds\\staff.json")
    return "Staff added succesfully"
@app.route("/add_item")
def add_item():
    fill_items("C:\\Users\\lenovo\\Documents\\DSOC\\winter24\\seeds\\items.json")
    return "Items added succesfully"
@app.route("/add_transaction")
def add_txn():
    fill_txn("C:\\Users\\lenovo\\Documents\\DSOC\\winter24\\seeds\\transactions.json")
    return "Transactions added succesfully"
# Route to Fetch All Transactions
@app.route("/transactions")
def transactions():
    with app.app_context():
        all_transactions = Transaction.query.all()
        result = ""
        for txn in all_transactions:
            result += f"{txn}<br>"
        return result or "No transactions found."
@app.route("/customers")
def customer_list():
    with app.app_context():
        all_customers=Customer.query.all()
        result=""
        for i in all_customers:
            result+=f"{i}<br>"
        return result or "No Customers found"
@app.route("/staff")
def staff_list():
    with app.app_context():
        all_staff=Staff.query.all()
        result=""
        for i in all_staff:
            result+=f"{i}<br>"
        return result or "No Staff found"
@app.route("/clear")
def abc():
    with app.app_context():
        db.drop_all()
        db.create_all()
        return "Database reset"

# Run the Flask App
if __name__ == "__main__":
    app.run(debug=True)





