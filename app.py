from flask import Flask, render_template, request, redirect, url_for
# from pymongo import MongoClient
app = Flask(__name__)

content = [
    { "candy name": "ABCD", "candy cost": "12", "url": "some url 1"},
    { "candy name": "CDEFG", "candy cost": "26", "url": "some url 2"}
]

@app.route("/")
def index():
    return render_template("home.html", msg="faslk is stpd")

if __name__ == "__main__":
    app.run(debug=True)