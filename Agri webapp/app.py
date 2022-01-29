from werkzeug.security import generate_password_hash
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

@app.route('/')
def homePage():
    dbAct.clearCart()
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
            crops = ()
            crops = dbAct.getAllCrops(session["user_id"])
            return render_template("farmerHome.html", crops=crops)
        else:
            return render_template("index.html", status1 = flag)
    crops = ()
    crops = dbAct.getAllCrops(session["user_id"])
    return render_template("farmerHome.html", crops=crops)

class InsertForRegistration:
    def __init__(self,name,password,phno):
        self.name = name
        self.password = password
        self.phno = phno

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

cartKeys = []
carts = ()
cart = {}

def fetchCart():
    carts = dbAct.getCart()
    for i in carts:
        cart[i[0]]= i[1]
        cartKeys.append(i[0])
fetchCart()

def clearCartBuffer():
    cartKeys.clear()
    cart.clear()

@app.route('/retailersHomePage', methods=["POST", 'GET'])
def retailersPage():
    fetchCart()
    if request.method == "POST":
        flag=0
        user = User()
        user.name = request.form["username"]
        user.password = request.form["password"]
        flag = dbAct.check_login_retailers(user)
        if flag == 1:
            session["user_id"]=user.id
            products = dbAct.getProducts()
            return render_template("retailersHome.html", products = products, cart=cart, cartKeys=cartKeys)
        else:
            return render_template("index.html", status2 = flag)
    products = dbAct.getProducts()
    return render_template("retailersHome.html", products = products, cart=cart, cartKeys=cartKeys)

class Crop:
    cName = ""
    quantity = 0
    price = 0
    imgLocation = ""
    desc= ""

@app.route("/updatestock", methods=["GET","POST"])
def updateStock():
    crops = ['Sona Masoori Rice', 'Basmati Rice', 'Brown Rice', 'Toor Dal', 'Chana Dal', 'Urad Dal', 'Green Moong Dal', 'Moong Dal', 'Rajma', 'Moong Dal', 'Groundnut', 'Groundnut Oil', 'Sunflower Oil', 'Bengal Gram', 'Kabuli Chana', 'Wheat', 'Wheat Flour', 'Rice Flour']
    if request.method == "POST":
        if request.form["crop"] not in crops:
            flash("Please choose a crop from the list")
            return render_template("updateStock.html", crops = crops)
        crop = Crop()
        crop.cName = request.form["crop"]
        crop.quantity = request.form["quantity"]
        crop.price = request.form["price"]
        crop.desc = request.form["cropDesc"]
        dbAct.addCrop(crop,session["user_id"])
        return redirect(url_for('farmersPage'))
    return render_template("updateStock.html", crops = crops)

@app.route("/deletecrop/<name>")
def deleteCrop(name):
    dbAct.deleteCrop(name)
    flash(f"{name} is removed successfully.")
    return redirect(url_for('farmersPage'))

@app.route("/profilefarmer")
def profileFarmer():
    det = dbAct.getLand(session["user_id"])
    fdata = dbAct.getFarmer(session["user_id"])
    return render_template("profileF.html", land = det, fdata=fdata)

class Land():
    regNo= ""
    area = 0
    district = ""

@app.route("/addland", methods=["POST", "GET"])
def allLand():
    districts = ['Bengaluru Rural', 'Shivamogga', 'Chikmagalur', 'Raichur']
    if request.method == "POST":
        if request.form["district"] not in districts:
            flash("Please choose a district from the list")
            return render_template("updateStock.html", districts = districts)
        land = Land()
        land.regNo = request.form["regno"]
        land.area = request.form["area"]
        land.district = request.form["district"]
        dbAct.addLand(land,session["user_id"])
        return redirect(url_for('profileFarmer'))
    return render_template("addLand.html", districts = districts)

@app.route("/aboutus")
def aboutUs():
    return render_template("aboutUs.html")

@app.route("/aboutusr")
def aboutUsR():
    return render_template("aboutUsR.html")

@app.route("/addtocart/<int:pid>")
def addtoCart(pid):
    fetchCart()
    products = dbAct.getProducts()
    if pid in cartKeys:
        for i in products:
            if i[0] == pid:
                q = i[4]
        if (cart[pid]+1)*100 > q:
            flash("Please Check Stock Availability before adding")
            return redirect(url_for('retailersPage'))
    dbAct.addCart(pid)
    if pid not in cart.keys():
        cartKeys.append(pid)
    fetchCart()
    return redirect(url_for('retailersPage'))

@app.route("/decreaseQ/<pid>")
def incrementQuantity(pid):
    val = cart[int(pid)]
    if val == 1:
        cartKeys.remove(int(pid))
        cart[int(pid)] = 0
    if not val:
        flash("You dont have this product in your cart!")
        return redirect(url_for('retailersPage'))
    dbAct.deleteCart(pid)
    fetchCart()
    return redirect(url_for('retailersPage'))

@app.route("/gotocart")
def goToCart():
    products = dbAct.getProducts()
    fetchCart()
    return render_template("cart.html", products = products, cart=cart)

@app.route("/ordercomplete")
def placeOrder():
    carts = dbAct.getCart()
    dbAct.placeOrder(carts, session["user_id"])
    flash("Order Placed! Please visit our center in 6-8 days to collect your order.")
    clearCartBuffer()
    return redirect(url_for('retailersPage'))

@app.route("/profileRetailer")
def profileRetailer():
    det = dbAct.getOrderDetails(session["user_id"])
    rdata = dbAct.getRetailer(session["user_id"])
    return render_template("profileR.html", rdata=rdata, det=det)

@app.route('/logout')
def logout():
    clearCartBuffer()
    dbAct.clearCart()
    session["user_id"] = None
    return redirect(url_for('homePage'))

if __name__ == "__main__":
    app.run(debug=True)

# cart = []
# class CartList:
#     def __init__(self, fid, loct, name, quantity, price, reqQ):
#         f_id = fid
#         loc = loct
#         crop = name
#         totQ = quantity
#         iprice = price
#         requiredQuantity = reqQ

# @app.route("/addtocart/<fid>/<loc>/<name>/<quantity>/<price>")
# def addtoCart(fid, loc, name, quantity, price):
#     if requiredQ == 0:
#         flash("Please enter required quantity.")
#         return redirect(url_for('retailersPage'))
#     cart.append(CartList(int(fid), loc, name, int(quantity), int(price), requiredQ))
#     print(cart)
#     flash(f"{name} is added to cart successfully.")
#     return redirect(url_for('retailersPage'))

# @app.route("/addthiscrop", methods=["POST", "GET"])
# def addThisCrop():
#     if request.method == "POST":
#         global requiredQ
#         requiredQ = request.form["qreq"]
#     return redirect(url_for('retailersPage'))