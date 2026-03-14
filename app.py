from flask import Flask

from models import db
from routesMeals import mealBp


def createApp():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    app.register_blueprint(mealBp)

    @app.errorhandler(404)
    def resourceNotFound(error):
        return {"error": "The requested URL or resource was not found."}, 404

    @app.errorhandler(500)
    def internalServerError(error):
        return {"error": "An unexpected error occurred on the server."}, 500

    return app


if __name__ == "__main__":
    app = createApp()
    app.run(debug=True)
