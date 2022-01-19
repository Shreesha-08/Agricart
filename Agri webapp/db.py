from flask import Flask
from flask_mysqldb import MySQL
from werkzeug.security import check_password_hash
from datetime import date

today = date.today()

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

    def addLand(self, land, fid):
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO land (land_reg_no, area, loc, f_id) VALUES (%s, %s, %s, %s)", (land.regNo, land.area, land.district, fid))
        mysql.connection.commit()
        cur.close()

    def getLand(self,fid):
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM land WHERE f_id=%s", [fid])
        landDetails = cur.fetchall()
        cur.close()
        return landDetails

    def getFarmer(self, fid):
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM farmers where f_id=%s", [fid])
        data = cur.fetchall()
        cur.close()
        return data

    def getProducts(self):
        cur = mysql.connection.cursor()
        cur.callproc("getProduct")
        products = cur.fetchall()
        cur.close()
        return products

    def getRetailer(self, cid):
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM customers where c_id=%s", [cid])
        data = cur.fetchall()
        cur.close()
        return data

    def addCart(self, item):
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM cart where pid=%s", [item])
        exists = cur.fetchall()
        if exists:
            updatedQ = exists[0][1] + 1
            cur.execute("UPDATE cart SET quantity=%s where pid=%s", (updatedQ, item))
        else:
            cur.execute("INSERT INTO cart values(%s,%s)", (item, 1))
        mysql.connection.commit()
        cur.close()

    def deleteCart(self, item):
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM cart where pid=%s", [item])
        exists = cur.fetchall()
        if exists[0][1] == 1:
            cur.execute("DELETE FROM cart WHERE pid=%s",[item])
        else:
            updatedQ = exists[0][1] - 1
            cur.execute("UPDATE cart SET quantity=%s where pid=%s", (updatedQ, item))
        mysql.connection.commit()
        cur.close()

    def getCart(self):
        with app.app_context():
            cur = mysql.connection.cursor()
            cur.execute("SELECT * FROM cart")
            exists = cur.fetchall()
            cur.close()
            return exists

    def placeOrder(self, cart, cid):
        d1 = today.strftime(r"%Y-%m-%d")
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO orderpk values()")
        cur.execute("SELECT MAX(order_id) FROM orderpk")
        oID = cur.fetchone()
        for items in cart:
            cur.execute("SELECT * FROM products WHERE stock_no=%s", [items[0]])
            data = cur.fetchone()
            p = data[5] * items[1]
            cur.execute("INSERT INTO orders(order_id, crops, quantity, price, c_id, f_id, pick_up_loc, ordered_date) values(%s,%s,%s,%s,%s,%s,%s,%s)", (oID[0], data[3], items[1]*100, p, cid, data[1], data[2], d1))
            cur.execute("SELECT * FROM stock WHERE stock_no=%s", [items[0]])
            stockData = cur.fetchone()
            qAvailable = stockData[3] - items[1]*100
            if qAvailable == 0:
                cur.execute("DELETE FROM stock WHERE stock_no=%s", [items[0]])
            else:
                cur.execute("UPDATE stock SET quantity=%s WHERE stock_no=%s", (qAvailable, items[0]))
        cur.execute("DELETE FROM cart where pid>0")
        mysql.connection.commit()
        cur.close()

    def clearCart(self):
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM cart where pid>0")
        mysql.connection.commit()
        cur.close()

    def getOrderDetails(self,cid):
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM orders where c_id=%s",[cid])
        cdata = cur.fetchall()
        cur.close()
        return cdata

dbAct = DatabaseActivities()