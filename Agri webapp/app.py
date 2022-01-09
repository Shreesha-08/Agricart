from flask import Flask, render_template, request
app = Flask(__name__,template_folder='template')

@app.route('/')
def homePage():
    return render_template("index.html")

@app.route('/farmersHomePage', methods=["POST"])
def farmersPage():
    if request.method == "POST":
        if request.form["username"] == "shreesha":
            return "Hello"
        else:
            return render_template("index.html")

@app.route('/retailersHomePage', methods=["POST"])
def retailersPage():
    if request.method == "POST":
        if request.form["username"] == "shreesha":
            return "Hello"
        else:
            return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)