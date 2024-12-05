import os
import math
import requests 

from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from flask_migrate import Migrate
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
    
def get_location(ip_address):
    # ipstack API key
    access_key = '2d8149e7aec4a74b26cdc232702b417e'
    
    # api url maken met ip adres
    url = f'http://api.ipstack.com/{ip_address}?access_key={access_key}'
    
    # request versturen en response opslaan
    response = requests.get(url)
    data = response.json() # omzetten naar json format
    
    return data


@app.route("/register", methods=["GET", "POST"])
def register():
    """Registeren nieuwe user."""
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
        
        # ww hashen
        hashed_password = generate_password_hash(password)

        # gebruiker zn ip pakken
        user_ip = request.remote_addr # ip addres
        location_data = get_location(user_ip)  # ipstack api gebruiken om met ip locatie data te verzamelen
        
        if not location_data or 'latitude' not in location_data or 'longitude' not in location_data: # als het niet lukt om ipaddres om te zetten naar data
            flash("Unable to find your location.", "error")
            return redirect(url_for("register"))
        
        # user zn latitude en longitude vast stellen
        user_lat = location_data['latitude'] 
        user_lon = location_data['longitude']

        # nieuwe user creeren en aan db toevoegen
        new_user = User(
            name=name,
            email=email,
            password=hashed_password,
            latitude=user_lat,
            longitude=user_lon
        )
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

UPLOAD_FOLDER = "static/uploads" # file met afbeelding van users
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"} # toegestane files

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

def allowed_file(filename):
    """Check om te kijken of foto aan eisen voldoet"""
    dot = '.' in filename

    if not dot:
        return False

    # 1x splitten bij puntje om extensie te pakken
    parts = filename.rsplit('.', 1)
    
    # check of er 2 delen zijn
    if len(parts) != 2:
        return False

    # file extensie pakken en lowercase zetten
    ext = name_parts[1].lower()

    # Check of the extensie in de toegestane lijst zit
    check = False
    if ext in ALLOWED_EXTENSIONS:
        check = True

    return check
    
@app.route("/create_task", methods=["GET", "POST"])
def create_task():
    """Pagina voor het aanmaken van een taak"""
    if request.method == "POST":
        title = request.form.get("title")
        description = request.form.get("description")
        location = request.form.get("location")
        photo = request.files.get("photo")
        
        if not title or not description or not location:
            flash("All fields are required!", "error")
            return redirect(url_for("create_task"))

        # lat en long van table ophalen van current user
        current_user = User.query.get(session["user_id"])
        user_lat = current_user.latitude
        user_lon = current_user.longitude
        
        # Als er een foto is geupload
        if photo and allowed_file(photo.filename):  # als extensie voldoet
            filename = secure_filename(photo.filename)
            photo_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            photo.save(photo_path)
        else:
            photo_path = None  # als er geen foto is
            
        # aan db toevoegen met latitude en longitude van de gebruiker
        new_task = Task(
            title=title,
            description=description,
            location=location,
            latitude=user_lat, # Latitude van de gebruiker
            longitude=user_lon, # Longitude van de gebruiker
            photo=photo_path,
            user_id=session["user_id"]
        )
        
        db.session.add(new_task)
        db.session.commit()

        flash("Task created successfully!", "success")
        return redirect(url_for("view_tasks"))

    return render_template("create_task.html")


def haversine(lat1, lon1, lat2, lon2):
    """wiskunde formule om van 2 verschillende lat en lon (x, y) afstand te berekenen"""
    # omzetten van latitude en longtitude van grade naar radius
    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)
    lat2 = math.radians(lat2)
    lon2 = math.radians(lon2)

    # verschil in coordinataen
    dlat = lat2 -lat1
    dlon = lon2 - lon1

    # Haversine formule
    a = math.sin(dlat / 2)**2 + math.cos(lat1) *math.cos(lat2)* math.sin(dlon /2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    # afstand berekenen
    R = 6371.0 # radius van aarde in km
    distance = R *c
    return distance


@app.route("/view_tasks")
def view_tasks():
    """pagina om tasks en bijbehornde afstander per gebruiker te laten zien"""
    # huidige gebruiker zijn lat en long ophalen van table
    current_user = User.query.get(session["user_id"])
    user_lat = current_user.latitude
    user_lon = current_user.longitude

    # alle tasks ophalen uit table
    tasks = Task.query.all()

    # lijst voor tasks en bijbehorende afstand
    tasks_distance = []

    # voor elke beschikbare task distance berekenen
    for task in tasks:
        task_lat = task.latitude
        task_lon = task.longitude
        distance = haversine(user_lat, user_lon, task_lat, task_lon)

        # task en bijbehorende afstand appenden aan lijst die we gaan displayen
        tasks_distance.append({
            'task': task,
            'distance': distance
        })

    return render_template("view_tasks.html", tasks_distance=tasks_distance)

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
    return render_template("chat.html")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)