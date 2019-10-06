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
    return render_template("new_car.html", car={}, title="New Car")

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

# This redirects becuase only need to update the car and not making new
@app.route("/cars/<car_id>", methods=["POST"])
def car_update_change(car_id):
    updated_car = {
         "model": request.form.get("model"),
        "cost": request.form.get("cost"),
        "url": request.form.get("url")       
    }
    cars.update_one(
        {"_id": ObjectId(car_id)},
        {"$set": updated_car})
    return redirect(url_for("car_show", passed_car_id=car_id))

@app.route("/cars/edit/<passed_car_id>")
def car_edit(passed_car_id):
    car = cars.find_one({"_id": ObjectId(passed_car_id)})
    return render_template("edit_car.html", car=car, title="Edit Car")

@app.route("/cars/<passed_car_id>/delete/", methods=["POST"])
def car_delete(passed_car_id):
    cars.delete_one({"_id": ObjectId(passed_car_id)})
    return redirect(url_for("cars_list"))

if __name__ == "__main__":
    app.run(debug=True)