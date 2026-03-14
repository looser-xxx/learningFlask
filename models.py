from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Meal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    foodName = db.Column(db.String(100), nullable=False)
    calories = db.Column(db.Integer, nullable=False)
    protein = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"<Meal {self.foodName}>"
