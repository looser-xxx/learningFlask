from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class Meal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    foodName = db.Column(db.String(100), nullable=False)
    calories = db.Column(db.Integer, nullable=False)
    protein = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"<Meal {self.foodName}>"


@app.route("/api/meals", methods=["GET", "POST"])
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

        output = []
        for meal in allMeals:
            output.append(
                {
                    "id": meal.id,
                    "foodName": meal.foodName,
                    "calories": meal.calories,
                    "protein": meal.protein,
                }
            )

        return {"count": len(output), "meals": output}, 200


@app.route("/api/meals/<int:id>", methods=["PUT", "DELETE"])
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


if __name__ == "__main__":
    app.run(debug=True)
