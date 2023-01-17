# Import all the necessary modules and packages
import os
from flask import Blueprint, render_template, redirect, url_for, request, flash, Flask
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from os.path import join, dirname, realpath
from . import db
from .models import User


auth = Blueprint("auth", __name__)

# Create the routs in web app

@auth.route("/login", methods=["GET","POST"])
def login():
    """This function redirecting users to the login page"""
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash("Logged in!", category="success")
                login_user(user, remember=True)
                return redirect(url_for("views.home"))
            else:
                flash("Password is incorrect." , category="error")
        else:
            flash("Email does not exist.", category="error")

    return render_template("login.html", user= current_user)


UPLOAD_FOLDER = "C:/Users/ION/Desktop/Python/Proiecte/Project_web_app/website/static/picture"
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "C:/Users/ION/Desktop/Python/Proiecte/Project_web_app/website/static/picture"

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@auth.route("/sign-up", methods=["GET","POST"])
def sign_up():
    """This function create a new user in the web aplication"""   
    if request.method == "POST":
        email = request.form.get("email")
        username = request.form.get("username")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")
        about = request.form.get("about")
        city = request.form.get("city")
        car = request.form.get("car")
        hobby = request.form.get("hobby")
        file1 = request.files.get("file1")         
        

        #if file and allowed_file(file.filename):
            #filename = secure_filename(file.filename)
            #file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))

        email_exists = User.query.filter_by(email=email).first()
        username_exists = User.query.filter_by(username=username).first()
        if email_exists:
            flash("Email is already in use.", category="error")
        elif username_exists:
            flash("Username is already in use.", category="error")
        elif password1 != password2:
            flash("Password don't match.", category="error")
        elif len(username) < 2:
            flash("Username is to short.", category="error")
        elif len(password1) < 8:
            flash("Password is to short", category="error")
        elif len(email) < 10:
            flash("Email is to short", category="error")
        else:
            file_name = file1.filename
            path = os.path.join(app.config['UPLOAD_FOLDER'], file1.filename)
            file1.save(path)

            new_user = User(email=email, username=username, \
                password=generate_password_hash(password1, method="sha256"), \
                about=about, car=car, city=city, hobby=hobby, file=file_name)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash("User was created!", category="success")
            return redirect(url_for("views.home"))

    return render_template("signup.html", user= current_user)


@auth.route("/logout")
@login_required
def logout():
    """This function redirecting users to the logout page"""
    logout_user()
    return redirect(url_for("views.home"))