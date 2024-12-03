import os
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from models import *

app = Flask(__name__)

if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route("/")
def index():
    """Homepage of the application"""
    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    """nieuwe gebruiker registereren"""
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")

        if not name or not email or not password:
            flash("All fields are required!", "error")
            return redirect(url_for("register"))

        hashed_password = generate_password_hash(password)
        new_user = User(name=name, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        flash("Account created successfully!", "success")
        return redirect(url_for("index"))

    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log in a user"""
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        
        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            session["user_id"] = user.id
            session["user_name"] = user.name
            flash(f"Welcome back, {user.name}!", "success")
            return redirect(url_for("homepage"))
        else:
            flash("Invalid login credentials.", "error")
            return redirect(url_for("login"))

    return render_template("login.html")

@app.route("/logout")
def logout():
    """Log out the current user"""
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for("index"))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)

@app.route("/")
def homepage():
    if 'user_id' not in session:
        # als user nog niet is ingelogd naar login sturen
        return redirect(url_for('login'))
    
    # als ingelogd is naar homepage
    return render_template('homepage.html')