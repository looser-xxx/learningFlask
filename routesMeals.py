from flask import Blueprint, request

from models import Meal, db

mealBp = Blueprint("mealBp", __name__)


# 2. Notice we use @mealBp.route now, instead of @app.route
@mealBp.route("/api/meals", methods=["GET", "POST"])
def handleMeals():
    if request.method == "POST":
        data = request.get_json()
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
        output = [
            {
                "id": m.id,
                "foodName": m.foodName,
                "calories": m.calories,
                "protein": m.protein,
            }
            for m in allMeals
        ]
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
