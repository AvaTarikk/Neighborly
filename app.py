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
    """beginpagine van website"""
    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    """nieuwe gebruiker registereren"""
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")
        
        if not name or not email or not password:
            flash("All fields are required!", "error")
            return redirect(url_for("register"))
        
        if password != confirm_password:
            flash("Passwords don't match!", "error")
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
    """log in user"""
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        
        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            session["user_id"] = user.id
            session["user_name"] = user.name
            flash(f"Welcome back, {user.name}!", "success")
            return redirect(url_for("index"))
        else:
            flash("Invalid login credentials.", "error")
            return redirect(url_for("login"))

    return render_template("login.html")

@app.route("/logout")
def logout():
    """Log out de huidige user"""
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for("index"))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
    
@app.route("/create_task", methods=["GET", "POST"])
def create_task():
    """Pagina voor het aanmaken van een taak"""
    if request.method == "POST":
        title = request.form.get("title")
        description = request.form.get("description")
        location = request.form.get("location")

        if not title or not description or not location:
            flash("All fields are required!", "error")
            return redirect(url_for("create_task"))

        new_task = Task(title=title, description=description, location=location, user_id=session["user_id"])
        db.session.add(new_task)
        db.session.commit()
        flash("Task created successfully!", "success")
        return redirect(url_for("view_tasks"))

    return render_template("create_task.html")

@app.route("/view_tasks")
def view_tasks():
    """Pagina voor het bekijken van alle taken"""
    tasks = Task.query.all()
    return render_template("view_tasks.html", tasks=tasks)

@app.route("/profile")
def profile():
    """Profielpagina van de huidige user"""
    if 'user_id' not in session:
        flash("Please log in to view your profile.", "warning")
        return redirect(url_for('login'))

    user = User.query.get(session["user_id"])
    return render_template("profile.html", user=user)

@app.route("/chat")
def chat():
    """Chatpagina voor communicatie"""
    if 'user_id' not in session:
        flash("Please log in to use the chat.", "warning")
        return redirect(url_for('login'))

    # Placeholder for actual chat functionality
    return render_template("chat.html")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)