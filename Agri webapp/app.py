from typing_extensions import ParamSpecKwargs
from werkzeug.security import generate_password_hash, check_password_hash
from db import *
from flask import Flask,flash, render_template, request, redirect, url_for
from flask_mysqldb import MySQL
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user

app = Flask(__name__,template_folder='template')

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '@0802root'
app.config['MYSQL_DB'] = 'agri'
app.secret_key = 'many random bytes'

mysql = MySQL(app)

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM farmers where f_id = {user_id}" )
    datas = cur.fetchall()
    cur.close()
    return datas

with app.app_context():
    cur = mysql.connection.cursor()
    cur.execute("SELECT  * FROM farmers")
    data = cur.fetchall()
    print(data)
    cur.close()

@app.route('/', methods=['GET'])
def homePage():
    return render_template("index.html")

class User(UserMixin):
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
            login_user(user)
            return render_template("registerF.html")
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

@app.route('/registerFarmers', methods=["POST", 'GET'])
def farmerRegister():
    if request.method == "POST":
        pw = request.form["psw"]
        hashedPassword = generate_password_hash(
            pw,
            method='pbkdf2:sha256',
            salt_length=3
        )
        print(hashedPassword)
        insertFarmers = InsertForRegistration(request.form["fname"], hashedPassword, request.form["phno"])
        dbAct.insert_to_farmers(insertFarmers)

@app.route('/registerRetailers', methods=["POST", 'GET'])
def retailerRegister():
    if request.method == "POST":
        if dbAct.check_for_user(request.form["rname"]):
            flash("Username already exists!")
            return render_template("registerR.html")
        hashedPassword = generate_password_hash(
            request.form.get('psw'),
            method='pbkdf2:sha256',
            salt_length=3
        )
        insertRetailer = InsertForRegistration(request.form["rname"], hashedPassword, request.form["phno"])
        dbAct.insert_to_retailers(insertRetailer)
    return render_template("registerR.html")

@app.route('/retailersHomePage', methods=["POST", 'GET'])
def retailersPage():
    if request.method == "POST":
        user = User()
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM customers WHERE c_name=%s",[request.form["username"]])
        usr = cur.fetchall()
        user.id = int(usr[0][0])
        user.name = usr[0][1]
        user.password = usr[0][2]
        print(user)
        cur.close()
        if not user.name:
            flash("Username does not exist, please try again.")
            return render_template("index.html")
        elif not check_password_hash(user.password, request.form["password"]):
            flash('Password incorrect, please try again.')
            return redirect(url_for('login'))
        else:
            # flag=0
            # user = User()
            # user.name = request.form["username"]
            # user.password = request.form["password"]
            # flag = dbAct.check_login_retailers(user)
            # if flag == 1:
            login_user(user)
            return render_template("retailerLogin.html")
    return render_template("index.html")

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True)