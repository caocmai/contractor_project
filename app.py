from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient

client = MongoClient()
db = client.contractor_project
cart = db.cart

app = Flask(__name__)

# cart = [
#     { "candy_name": "ABCD", "cost": "12", "url": "some url 1"},
#     { "candy_name": "CDEFG", "cost": "26", "url": "some url 2"}
# ]

# @app.route("/")
# def index():
#     return render_template("home.html", msg="faslk is stpd")

@app.route("/")
def content_list():
    return render_template("list.html", cart=cart.find())

if __name__ == "__main__":
    app.run(debug=True)