# Import all the necessary modules and packages
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from . import db
from .models import User, Post, Comment

views = Blueprint("views", __name__)

# Create the routs in web app

@views.route("/")
@views.route("/home")
def home():
    """This function redirecting users to the home page"""
    posts = Post.query.all()
    return render_template("home.html", user= current_user, posts=posts)


@views.route("/create-post", methods=["GET", "POST"])
@login_required
def create_post():
    """Thist function create a post"""
    if request.method == "POST":
        text = request.form.get("text")

        if not text:
            flash("Post cannot be empty.", category="error")
        else:
            post = Post(text=text, author=current_user.id)
            db.session.add(post)
            db.session.commit()
            flash("Post was created.", category="success")
            return redirect (url_for("views.home"))
    
    return render_template("create_post.html", user = current_user)


@views.route("/delete-post/<id>", methods=["GET", "POST"])
@login_required
def delete_post(id):
    """This function delete user post"""
    post = Post.query.filter_by(id=id).first()

    if not post:
        flash("Post does not exist.", category="error")
    elif current_user.id != post.author:
        flash("You do not have permission to delete this post.", category="error")
    else:
        db.session.delete(post)
        db.session.commit()
        flash("Post was deleted.", category="success")
    return redirect(url_for("views.home"))


@views.route("/profile/<username>")
@login_required
def posts(username):
    """This function show all post for selected user"""
    user = User.query.filter_by(username=username).first()

    if not user:
        flash("No user with that username exists.", category="error")
        return redirect(url_for("views.home"))

    posts = Post.query.filter_by(author=user.id).all()
    return render_template("profile.html", user=current_user, posts=posts)


@views.route("/create-comment/<post_id>", methods=["POST"])
@login_required
def create_comment(post_id):
    """With this function user create a commnet under Post's, created by himself or other users."""
    text = request.form.get("text")

    if not text:
        flash("Comment cannot be empty.", category="error")
    else:
        post = Post.query.filter_by(id=post_id)
        if post:
            comment =Comment(text=text, author=current_user.id, post_id=post_id)
            db.session.add(comment)
            db.session.commit()
        else:
            flash("Post does not exist.", category="error")

    return redirect(url_for("views.home"))
        
    
@views.route("/about")
def about():
    """This function render template for about html page"""
    return render_template("about.html", user= current_user)


@views.route("/contact")
def contact():
    """This function render template for Contact html page"""
    return render_template("contact.html", user= current_user)
