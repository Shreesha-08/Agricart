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

@app.route('/')
def homePage():
    return render_template("index.html")
print(mysql.connection)
nam = []

@app.route('/farmersHomePage', methods=["POST"])
def farmersPage():
    if request.method == "POST":
        if request.form["username"] == "shreesha":
            newLogin = {request.form["username"]: request.form["password"]}
            nam.append(newLogin)
            print(nam)
            return "Hello"
        else:
            return render_template("index.html")

@app.route('/retailersHomePage', methods=["POST"])
def retailersPage():
    if request.method == "POST":
        name = request.form["username"]
        password = request.form["password"]
        phone = "90999"
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO farmers (f_name, f_pwd, ph_no) VALUES (%s, %s, %s)", (name, password, phone))
        mysql.connection.commit()
        return "redirect(url_for('index'))"

if __name__ == "__main__":
    app.run(debug=True)