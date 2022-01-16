from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
import re

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
    cur.execute("SELECT  * FROM stock")
    sdata = cur.fetchall()
    cur.close()

class DatabaseActivities:
    def insert_to_farmers(self,obj):
        with app.app_context():
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO farmers (f_name, f_pwd, ph_no) VALUES (%s, %s, %s)", (obj.name, obj.password, obj.phno))
            mysql.connection.commit()
            cur.close()
    
    def insert_to_retailers(self,obj):
        with app.app_context():
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO customers (c_name, c_pwd, ph_no) VALUES (%s, %s, %s)", (obj.name, obj.password, obj.phno))
            mysql.connection.commit()
            cur.close()

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
    
    def get_cid(self, usr):
        cur = mysql.connection.cursor()
        cur.execute("SELECT c_id FROM customers WHERE c_name=%s",usr)
        cid = cur.fetchall()
        cur.close()
        return cid

    def check_for_userF(self,usr):
        cur = mysql.connection.cursor()
        cur.execute("SELECT  * FROM farmers WHERE f_name=%s",[usr])
        flag = cur.fetchall()
        cur.close()
        if flag:
            return True
        else:
            return False

    def check_for_userC(self,usr):
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM customers WHERE c_name=%s",[usr])
        flag = cur.fetchall()
        cur.close()
        if flag:
            return True
        else:
            return False

    def addCrop(self, crop, fid):
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM stock WHERE f_id=%s AND crop=%s",(fid, crop.cName))
        exists = cur.fetchall()
        crop.imgLocation = '../static/images/'+ (crop.cName).replace(" ", "") +'.jpg'
        print(crop.imgLocation)
        if exists:
            updatedQuantity = int(crop.quantity) + int(exists[0][2])
            updatedPrice = int(crop.price) + int(exists[0][3])
            cur.execute("UPDATE stock SET quantity=%s, price=%s, description=%s WHERE f_id=%s AND crop=%s", (updatedQuantity, updatedPrice, crop.desc, fid, crop.cName))
            mysql.connection.commit()
        else:
            cur.execute("INSERT INTO stock (crop, f_id, quantity, price, imgLocation, description) VALUES (%s, %s, %s, %s, %s, %s)", (crop.cName, fid, int(crop.quantity), int(crop.price), crop.imgLocation, crop.desc))
            mysql.connection.commit()
        cur.close()
        
    def getAllCrops(self, fid):
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM stock WHERE f_id=%s", [fid])
        allCrops = cur.fetchall()
        cur.close()
        return allCrops

    def deleteCrop(self,cName):
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM stock WHERE crop=%s", [cName])
        mysql.connection.commit()
        cur.close()

dbAct = DatabaseActivities()