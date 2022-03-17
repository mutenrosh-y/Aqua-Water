from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from tempfile import mkdtemp

from sqlalchemy import null
app = Flask(__name__)
Bootstrap(app)
db = SQL('sqlite:///water.db')


@app.route('/', methods=['POST', 'GET'],)
def Dashobard():
    return render_template('index.html')


@app.route('/insert/', methods=['POST', 'GET'],)
def viewInsert():
    if request.method == 'GET':
        return render_template('insert.html')


@app.route('/insert/customer', methods=['POST', 'GET'],)
def insertCustomer():

    customerid = request.form.get("customerid")
    if len(customerid) != 5:
        return render_template('insert.html', error="Invalid Customer ID")

    customerValid = db.execute(
        "SELECT Customer_ID FROM customer WHERE Customer_ID = :customerid", customerid=customerid)
    if (customerValid):
        return render_template('insert.html', error="Customer ID already in use")

    phonenumber = request.form.get("primaryphone")
    if len(phonenumber) != 10:
        return render_template('insert.html', error="Invalid Mobile Number")


    db.execute("INSERT INTO customer VALUES(:customerid, :firstname, :lastname, :phonenumber)",
               customerid=request.form.get("customerid"), firstname=request.form.get("firstname"), lastname=request.form.get("lastname"),
               phonenumber=request.form.get("primaryphone"))
    return render_template('insert.html')


@app.route('/insert/sim', methods=['POST', 'GET'],)
def insertSim():

    db.execute("INSERT INTO product VALUES(:productid, :productname, :unitprice, :quantity, :customerid)",
               productid=request.form.get("productid"), productname=request.form.get("productname"),
               unitprice=request.form.get("unitprice"), quantity=request.form.get("quantity"),customerid=request.form.get("customerid") )
    return render_template('insert.html')



@app.route('/customer/', methods=['POST', 'GET'],)
def searchCustomer():
    if request.method == 'GET':
        return render_template('customer.html')
    else:
        search = request.form['customerid']
        records = db.execute(
            "SELECT * FROM customer where customer_id = :customerid", customerid=search)
        return render_template('customer.html', records=records)


@app.route('/sim/', methods=['POST', 'GET'],)
def searchSIM():
    if request.method == 'GET':
        return render_template('sim.html')
    else:
        search = request.form['customerid']
        records = db.execute(
            "SELECT * FROM product where customer_id = :customerid", customerid=search)
        return render_template('sim.html', records=records)


# @app.route('/calllog/', methods=['POST', 'GET'],)
# def searchCall():
#     if request.method == 'GET':
#         return render_template('calllog.html')
#     else:
#         search = request.form['simid']
#         records = db.execute(
#             "SELECT * FROM calllogs where SIM_ID = :simid", simid=search)
#         return render_template('calllog.html', records=records)


# @app.route('/update/', methods=['POST', 'GET'],)
# def viewUpdate():
#     return render_template('update.html')


# @app.route('/update/customer', methods=['POST', 'GET'],)
# def updateCustomer():
#     if request.method == 'POST':
#         if request.form['Button'] == "Load":
#             search = request.form['customerid']
#             customerValid = db.execute(
#                 "SELECT Customer_ID FROM customer WHERE Customer_ID = :customerid", customerid=search)
#             if (not customerValid):
#                 return render_template('update.html', error="Customer ID does not exist")
#             records = db.execute(
#                 "SELECT * FROM customer where customer_id = :customerid", customerid=search)
#             firstname = records[0]['First_Name']
#             lastname = records[0]['Last_Name']
#             phone = records[0]['Contact_no']
#             return render_template('update.html', firstname=firstname, lastname=lastname,
#                                    phone=phone, customerid=search)
#         else:
#             phonenumber = request.form["primaryphone"]
#             if len(phonenumber) != 10:
#                 return render_template('update.html', error="Invalid Mobile Number")

#             db.execute("UPDATE customer SET First_Name = :firstname, Last_Name = :lastname, Contact_no = :primaryphone WHERE Customer_ID = :customerid", customerid=int(
#                 request.form["customerid"]), firstname=request.form["firstname"], lastname=request.form["lastname"], primaryphone=int(request.form["primaryphone"]))
#             return render_template('update.html')
#     else:
#         return render_template('update.html')


# @app.route('/update/sim', methods=['POST', 'GET'],)
# def updateSim():
#     if request.method == 'POST':
#         if request.form['Button'] == "Load":
#             search = request.form["simid"]
#             simValid = db.execute(
#                 "SELECT SIM_ID FROM sim WHERE SIM_ID = :simid", simid=search)
#             if (not simValid):
#                 return render_template('update.html', error="SIM ID does not exist")

#             records = db.execute(
#                 "SELECT status FROM SIM where SIM_ID = :simid", simid=search)
#             status = records[0]['Status']
#             return render_template('update.html', simid=search, status=status)
#         else:
#             db.execute("UPDATE sim SET Status = :status WHERE SIM_ID = :simid", simid=int(
#                 request.form["simid"]), status=request.form["status"])
#             return render_template('update.html')
#     else:
#         return render_template('update.html')


if __name__ == '__main__':
    app.run(debug=True)
