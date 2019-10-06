from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId

client = MongoClient()
db = client.contractor_project
cars = db.cars

app = Flask(__name__)

# cart = [
#     { "candy_name": "ABCD", "cost": "12", "url": "some url 1"},
#     { "candy_name": "CDEFG", "cost": "26", "url": "some url 2"}
# ]

# @app.route("/")
# def index():
#     return render_template("home.html", msg="faslk is stpd")

@app.route("/")
def cars_list():
    return render_template("cars_index.html", cars=cars.find())

@app.route("/cars/new")
def new_car():
    return render_template("new_car.html")

@app.route("/cars/delete_all")
def delete_all():
    cars.remove()
    return redirect(url_for("cars_list"))

@app.route("/new_car", methods=["POST"])
def new_car_submit():
    car = {
        "model": request.form.get("model"),
        "cost": request.form.get("cost"),
        "url": request.form.get("url")
    }
    car_id = cars.insert_one(car).inserted_id
    return redirect(url_for("car_show", passed_car_id=car_id))

@app.route("/cars/<passed_car_id>")
def car_show(passed_car_id):
    car = cars.find_one({"_id": ObjectId(passed_car_id)})
    return render_template("single_car.html", car=car)



if __name__ == "__main__":
    app.run(debug=True)