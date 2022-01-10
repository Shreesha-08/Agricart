from typing_extensions import ParamSpecKwargs
from db import *
from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL

app = Flask(__name__,template_folder='template')

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '@0802root'
app.config['MYSQL_DB'] = 'agri'
app.secret_key = 'many random bytes'

mysql = MySQL(app)

with app.app_context():
    cur = mysql.connection.cursor()
    cur.execute("SELECT  * FROM farmers")
    data = cur.fetchall()
    print(data)
    cur.close()

@app.route('/')
def homePage():
    return render_template("index.html")

@app.route('/farmersHomePage', methods=["POST"])
def farmersPage():
    if request.method == "POST":
        if request.form["username"] == "shreesha":
            newLogin = {request.form["username"]: request.form["password"]}
            return "Hello"
        else:
            return render_template("index.html")

class InsertForRegistration:
    def __init__(self,name,password,phno):
        self.name = name
        self.password = password
        self.phno = phno

@app.route('/registerF.html')
def fRegPage():
    return render_template("registerF.html")

@app.route('/registerR.html')
def rRegPage():
    return render_template("registerR.html")

@app.route('/registerFarmers', methods=["POST"])
def farmerRegister():
    if request.method == "POST":
        insertFarmers = InsertForRegistration(request.form["fname"], request.form["psw"], request.form["phno"])
        dbAct.insert_to_farmers(insertFarmers)

@app.route('/registerRetailers', methods=["POST"])
def retailerRegister():
    if request.method == "POST":
        insertRetailer = InsertForRegistration(request.form["rname"], request.form["psw"], request.form["phno"])
        dbAct.insert_to_retailers(insertRetailer)

@app.route('/retailersHomePage', methods=["POST"])
def retailersPage():
    if request.method == "POST":
        return "Hello Buyer"

if __name__ == "__main__":
    app.run(debug=True)