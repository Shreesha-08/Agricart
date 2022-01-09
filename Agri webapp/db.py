from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL

app = Flask(__name__,template_folder='template')
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '@0802root'
app.config['MYSQL_DB'] = 'agri'

mysql = MySQL(app)

class DatabaseActivities:
    def insert_to_farmers(self,obj):
        phone = "90999"
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO farmers (f_name, f_pwd, ph_no) VALUES (%s, %s, %s)", (obj.name, obj.password, phone))
        mysql.connection.commit()
        return redirect(url_for('Index'))

dbAct = DatabaseActivities()