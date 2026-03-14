from flask import Flask, jsonify, request

app = Flask(__name__)

mealDatabase = []


@app.route("/api/meals", methods=["GET", "POST"])
def hello_world():
    if request.method == "POST":
        newMeal = request.get_json()
        mealDatabase.append(newMeal)
        return {"message": "Meal added succesfully!", "addedMeal": newMeal}, 201

    if request.method == "GET":
        return {"count": len(mealDatabase), "meals": mealDatabase}, 200


@app.route("/api/meals/<int:index>", methods=["GET"])
def getSingleMeal(index):
    try:
        meal = mealDatabase[index]
        return {"meal": meal}, 200
    except:
        return {"error": "meal not found"}, 404


if __name__ == "__main__":
    app.run(debug=True)
