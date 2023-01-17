# Import all the necessary modules and packages
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from os import path


db = SQLAlchemy()
DB_NAME = "database.db"


# This is the function for creating the web application
def create_app():
    """This Function creates the web application"""
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "MIN302"
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_NAME}"
    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix = "/")
    app.register_blueprint(auth, url_prefix = "/")

    from .models import User, Post, Comment, Like

    with app.app_context():
        db.create_all()
    
    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        """This function queries the database and returns all data related to the user using id"""
        return User.query.get(int(id))

    return app
