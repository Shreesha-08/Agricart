from flask import Flask, render_template, request

app = Flask(__name__,template_folder='template')

@app.route("/")
def hello_world():
    name = "bob"
    pwd = "alice"
    return render_template("index.html",name=name, pwd =pwd)

@app.route("/login", methods=["POST"])
def log_in():
    if request.method == "POST":
        name = request.form["username"]
        pwd = request.form["pwd"]
        return render_template("index.html", name=name, pwd =pwd)
    
@app.route("/retailer", methods=["POST"])
def logs_in():
    if request.method == "POST":
        name = request.form["username"]
        pwd = request.form["pwd"]
        return render_template("retailer.html", name=name)

if __name__ == "__main__":
    app.run(debug=True)