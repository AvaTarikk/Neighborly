import os
import math
import requests 

from flask import Flask, flash, redirect, render_template, request, session, url_for, jsonify
from flask_session import Session
from flask_migrate import Migrate
from werkzeug.security import check_password_hash, generate_password_hash
from models import *
from flask_socketio import SocketIO, emit, join_room

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

UPLOAD_FOLDER = "static/uploads/" # file met afbeelding van users
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
    ext = parts[1].lower()

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
        category = request.form.get('category')
        urgency = request.form.get('urgency')
        location = request.form.get("location")
        photo = request.files.get("photo")
                
        if not title or not description or not location or not category or not urgency:
            flash("All fields are required!", "error")
            return redirect(url_for("create_task"))

        # lat en long van table ophalen van current user
        current_user = User.query.get(session["user_id"])
        user_lat = current_user.latitude
        user_lon = current_user.longitude
        
        # Als er een foto is geupload
        photo_path = None
        if photo and allowed_file(photo.filename):
            photo_path = os.path.join(app.config['UPLOAD_FOLDER'], photo.filename)
            photo.save(photo_path)
            
        # aan db toevoegen met latitude en longitude van de gebruiker
        new_task = Task(
            title=title,
            description=description,
            category=category,
            urgency=urgency,
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
    
    # filters hendelen als die er zijn
    category_filter = request.args.get('category')
    urgency_filter = request.args.get('urgency')
    max_distance = request.args.get('distance', type=int)

    # filteren
    tasks_met_filter = Task.query

    # op categore filteren als erom gevraagd is
    if category_filter:
        tasks_met_filter = tasks_met_filter.filter(Task.category == category_filter)
    
    # op urgency filteren
    if urgency_filter:
        tasks_met_filter = tasks_met_filter.filter(Task.urgency == urgency_filter)
    
    # alle tasks ophalen uit table met of zonder filters
    tasks = tasks_met_filter.all()

    # lijst voor tasks en bijbehorende afstand
    tasks_distance = []

    # voor elke beschikbare task distance berekenen
    for task in tasks:
        task_lat = task.latitude
        task_lon = task.longitude
        distance = haversine(user_lat, user_lon, task_lat, task_lon)
    
        # als er gefiltered is om distancen en afstand is groter dan maxdistance skip
        if max_distance and distance > max_distance:
            continue # scot als distance groter is dan gelievde distance
            
        # als er geen mac distance is of distance valt binnen max distancen task appenden aan lijst
        tasks_distance.append({
            'task': task,
            'distance': distance
        })

    return render_template("view_tasks.html", tasks_distance=tasks_distance)

@app.route("/profile")
def profile():
    """Profielpagina van de huidige user"""
    user = User.query.get(session["user_id"])
    return render_template("profile.html", user=user)

socketio = SocketIO(app)

@app.route('/chat/<int:recipient_id>')
def chat(recipient_id):
    """chat pagina loaden voor specifieke hulpzoekende"""
    recipient = User.query.get(recipient_id)

    # chat history ophalen
    user_id = session['user_id']
    messages = Message.query.filter(
        ((Message.sender_id == user_id) & (Message.recipient_id == recipient_id)) |
        ((Message.sender_id == recipient_id) & (Message.recipient_id == user_id))
    ).order_by(Message.timestamp).all()

    return render_template('chat.html', recipient=recipient, messages=messages)

@app.route('/upload', methods=['POST'])
def upload_file():
    """fucntien als user een file of foto wilt delen"""
    file = request.files.get('file')
    if file:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
        return jsonify({'file_url': filepath})

@socketio.on('send_message')
def handle_send_message(data):
    """Process sent messages."""
    sender_id = session.get('user_id')
    recipient_id = data.get('recipient_id')
    message_tekst = data.get('message')
    bestand = data.get('file')

    # message opslaan in db
    message = Message(
        sender_id=sender_id,
        recipient_id=recipient_id,
        message=message_tekst,
        file=bestand,
        is_read=False,
        task_id=task_id
    )
    db.session.add(message)
    db.session.commit()

    # bericht naar ontvanger sturen
    emit('receive_message', {
        'sender_id': sender_id,
        'recipient_id': recipient_id,
        'message': message_tekst,
        'file': bestand,
        'timestamp': message.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
        'is_read': False,
        'task_id': task_id
    }, room=f'user_{recipient_id}')
    
    # bericht naar verzender zelf sturen zodat hij hem zelf ook meteen in de chat kan zien
    emit('receive_message', {
        'sender_id': sender_id,
        'recipient_id': recipient_id,
        'message': message_tekst,
        'file': bestand,
        'timestamp': message.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
        'is_read': False,
        'task_id': task_id
    }, room=f'user_{sender_id}')
    
@app.route('/mark_read/<int:sender_id>', methods=['POST'])
def mark_read(sender_id):
    """Mark messages from a specific sender as read."""
    user_id = session.get('user_id')

    # ongelezen messages ophalen en op geread zetten als session user id gelijk is aan ontvanger
    messages = Message.query.filter_by(sender_id=sender_id, recipient_id=user_id, is_read=False).all()
    for message in messages: # op true zetten
        message.is_read = True
    db.session.commit()

    return jsonify({'success': True})

@socketio.on('join')
def handle_join(data):
    """chat joinen met een bepaalde user"""
    user_id = session.get('user_id')
    if user_id:
        join_room(f'user_{user_id}')
        
@app.route('/chats', methods=['GET'])
def chats():
    user_id = session['user_id']
    # sql query om alle tasks en de messages daarvan te pakken waar de user in zit
    tasks = Task.query.filter(
        (Task.user_id == user_id) | (Task.id.in_(db.session.query(Message.task_id)
        .filter((Message.sender_id == user_id) | (Message.recipient_id == user_id))))).all()

    # chats aanmaken voor elke task en behorende deelenemers
    chats = {}
    for task in tasks:
        messages = Message.query.filter_by(task_id=task.id).order_by(Message.timestamp.desc()).all()
        chat_participants = {
            message.sender_id if message.sender_id != user_id else message.recipient_id
            for message in messages
        }
        
        for ander in chat_participants:
            if ander != user_id: # je wilt de andere deelnemer pakken
                participant = User.query.get(ander)
                if task.id not in chats: # als er nog geen chat al is voor een taak maken we eentje aan
                    chats[task.id] = {
                        'task': task,
                        'participants': []
                    }
                chats[task.id]['participants'].append({
                    'user': participant,
                    'last_message': messages[0] if messages else None
                })

    return render_template('chats.html', chats=chats)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
    
    socketio.run(app)