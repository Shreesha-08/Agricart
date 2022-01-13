from typing_extensions import ParamSpecKwargs
from werkzeug.security import generate_password_hash, check_password_hash
from db import *
from flask import Flask, flash, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL

app = Flask(__name__,template_folder='template')

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '@0802root'
app.config['MYSQL_DB'] = 'agri'

mysql = MySQL(app)
app.secret_key = 'aight'

with app.app_context():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM farmers")
    data = cur.fetchall()
    print(data)
    cur.close()

@app.route('/')
def homePage():
    return render_template("index.html")

class User():
    id= ""
    name = ""
    password = ""

@app.route('/farmersHomePage', methods=["POST", 'GET'])
def farmersPage():
    if request.method == "POST":
        flag=0
        user = User()
        user.name = request.form["username"]
        user.password = request.form["password"]
        flag = dbAct.check_login_farmers(user)
        if flag == 1:
            session["user_id"]=user.id
            return render_template("farmerHome.html")
        else:
            return render_template("index.html", status1 = flag)

class InsertForRegistration:
    def __init__(self,name,password,phno):
        self.name = name
        self.password = password
        self.phno = phno

# @app.route('/registerF.html')
# def fRegPage():
#     return render_template("registerF.html")

# @app.route('/registerR.html')
# def rRegPage():
#     return render_template("registerR.html")

@app.route('/registerFarmers', methods=["POST", 'GET'])
def farmerRegister():
    if request.method == "POST":
        if dbAct.check_for_userF(request.form["fname"]):
            flash("Username already exists!")
            return render_template("registerF.html")
        pw = request.form["psw"]
        hashedPassword = generate_password_hash(
            pw,
            method='pbkdf2:sha256',
            salt_length=3
        )
        insertFarmers = InsertForRegistration(request.form["fname"], hashedPassword, request.form["phno"])
        dbAct.insert_to_farmers(insertFarmers)
        return redirect("/")
    return render_template("registerF.html")

@app.route('/registerRetailers', methods=["POST", 'GET'])
def retailerRegister():
    if request.method == "POST":
        if dbAct.check_for_userC(request.form["rname"]):
            flash("Username already exists!")
            return render_template("registerR.html")
        hashedPassword = generate_password_hash(
            request.form.get('psw'),
            method='pbkdf2:sha256',
            salt_length=3
        )
        insertRetailer = InsertForRegistration(request.form["rname"], hashedPassword, request.form["phno"])
        dbAct.insert_to_retailers(insertRetailer)
        return redirect('/')
    return render_template("registerR.html")

@app.route('/retailersHomePage', methods=["POST", 'GET'])
def retailersPage():
    if request.method == "POST":
        flag=0
        user = User()
        user.name = request.form["username"]
        user.password = request.form["password"]
        flag = dbAct.check_login_retailers(user)
        if flag == 1:
            session["user_id"]=user.id
            return render_template("retailerLogin.html")
        else:
            return render_template("index.html", status2 = flag)

@app.route('/logout')
def logout():
    # logout_user()
    session["user_id"] = None
    return redirect(url_for('homePage'))

if __name__ == "__main__":
    app.run(debug=True)