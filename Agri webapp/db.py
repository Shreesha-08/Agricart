from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__,template_folder='template')
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '@0802root'
app.config['MYSQL_DB'] = 'agri'

mysql = MySQL(app)

with app.app_context():
    cur = mysql.connection.cursor()
    cur.execute("SELECT  * FROM farmers")
    fdata = cur.fetchall()
    cur.execute("SELECT  * FROM customers")
    rdata = cur.fetchall()
    cur.close()

class DatabaseActivities:
    def insert_to_farmers(self,obj):
        with app.app_context():
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO farmers (f_name, f_pwd, ph_no) VALUES (%s, %s, %s)", (obj.name, obj.password, obj.phno))
            mysql.connection.commit()
            return render_template("index")
    
    def insert_to_retailers(self,obj):
        with app.app_context():
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO customers (c_name, c_pwd, ph_no) VALUES (%s, %s, %s)", (obj.name, obj.password, obj.phno))
            mysql.connection.commit()
            return render_template("index")

    def check_login_farmers(self,details):
        flag=0
        j=0
        while j < len(fdata):
            if check_password_hash(fdata[j][2], details.password) and (details.name==fdata[j][1]):
                details.id = fdata[j][0]
                flag=1
            j+=1
        return flag
    
    def check_login_retailers(self,details):
        flag=0
        j=0
        print(rdata)
        while j < len(rdata):
            if check_password_hash(rdata[j][2], details.password) and (details.name==rdata[j][1]):
                details.id = rdata[j][0]
                flag=1
            j+=1
        return flag
    
    def get_pwd(self, usr):
        cur = mysql.connection.cursor()
        cur.execute("SELECT  * FROM customers WHERE c_name=%s",[usr])
        pwd = cur.fetchall()
        cur.close()
        print(pwd)
        return pwd[0][2]

    def check_for_user(self,usr):
        cur = mysql.connection.cursor()
        cur.execute("SELECT  * FROM customers WHERE c_name=%s",[usr])
        flag = cur.fetchall()
        cur.close()
        if flag:
            return True
        else:
            return False

dbAct = DatabaseActivities()