from flask import Blueprint, request

from models import Meal, db

mealBp = Blueprint("mealBp", __name__)


@mealBp.route("/api/meals", methods=["GET", "POST"])
def handleMeals():
    if request.method == "POST":
        data = request.get_json()

        if not data:
            return {"error": "No input data provided."}, 400

        if "foodName" not in data or "calories" not in data or "protein" not in data:
            return {
                "error": "Missing required fields. Please provide foodName, calories, and protein."
            }, 400

        newMeal = Meal(
            foodName=data["foodName"],
            calories=data["calories"],
            protein=data["protein"],
        )

        db.session.add(newMeal)
        db.session.commit()
        return {"message": "Meal saved to database!", "id": newMeal.id}, 201

    if request.method == "GET":
        allMeals = Meal.query.all()

        output = []
        for currentMeal in allMeals:
            mealDictionary = {
                "id": currentMeal.id,
                "foodName": currentMeal.foodName,
                "calories": currentMeal.calories,
                "protein": currentMeal.protein,
            }
            output.append(mealDictionary)

        return {"count": len(output), "meals": output}, 200


@mealBp.route("/api/meals/<int:id>", methods=["PUT", "DELETE"])
def handleSingleMeal(id):
    meal = Meal.query.get_or_404(id)

    if request.method == "PUT":
        data = request.get_json()

        meal.foodName = data.get("foodName", meal.foodName)
        meal.calories = data.get("calories", meal.calories)
        meal.protein = data.get("protein", meal.protein)

        db.session.commit()
        return {"message": "Meal updated successfully!"}

    if request.method == "DELETE":
        db.session.delete(meal)
        db.session.commit()
        return {"message": f"Meal {id} has been deleted."}
