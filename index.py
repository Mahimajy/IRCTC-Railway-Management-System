# IRCTC Railway Management System

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from functools import wraps

app = Flask(__name__)

# Configurations
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///irctc.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Database Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(10), nullable=False)  # 'admin' or 'user'

class Train(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    source = db.Column(db.String(100), nullable=False)
    destination = db.Column(db.String(100), nullable=False)
    total_seats = db.Column(db.Integer, nullable=False)
    available_seats = db.Column(db.Integer, nullable=False)

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    train_id = db.Column(db.Integer, nullable=False)
    seat_number = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow)

# Helper Functions
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('x-access-token')
        if not token:
            return jsonify({'message': 'Token is missing!'}), 403

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = User.query.filter_by(id=data['id']).first()
        except:
            return jsonify({'message': 'Token is invalid!'}), 403

        return f(current_user, *args, **kwargs)

    return decorated

# Routes
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    hashed_password = generate_password_hash(data['password'], method='sha256')
    new_user = User(username=data['username'], password_hash=hashed_password, role=data['role'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User registered successfully!'})

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    if not user or not check_password_hash(user.password_hash, data['password']):
        return jsonify({'message': 'Invalid credentials!'}), 401

    token = jwt.encode({'id': user.id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)}, app.config['SECRET_KEY'], algorithm="HS256")
    return jsonify({'token': token})

@app.route('/admin/add_train', methods=['POST'])
def add_train():
    api_key = request.headers.get('x-api-key')
    if api_key != 'your_admin_api_key':
        return jsonify({'message': 'Unauthorized!'}), 403

    data = request.get_json()
    new_train = Train(name=data['name'], source=data['source'], destination=data['destination'], total_seats=data['total_seats'], available_seats=data['total_seats'])
    db.session.add(new_train)
    db.session.commit()
    return jsonify({'message': 'Train added successfully!'})

@app.route('/check_availability', methods=['GET'])
def check_availability():
    source = request.args.get('source')
    destination = request.args.get('destination')
    trains = Train.query.filter_by(source=source, destination=destination).all()
    results = [{'id': train.id, 'name': train.name, 'available_seats': train.available_seats} for train in trains]
    return jsonify(results)

@app.route('/book_seat', methods=['POST'])
@token_required
def book_seat(current_user):
    data = request.get_json()
    train = Train.query.filter_by(id=data['train_id']).first()

    if not train or train.available_seats <= 0:
        return jsonify({'message': 'No seats available!'}), 400

    train.available_seats -= 1
    new_booking = Booking(user_id=current_user.id, train_id=train.id, seat_number=train.total_seats - train.available_seats)
    db.session.add(new_booking)
    db.session.commit()
    return jsonify({'message': 'Seat booked successfully!', 'seat_number': new_booking.seat_number})

@app.route('/booking_details', methods=['GET'])
@token_required
def booking_details(current_user):
    bookings = Booking.query.filter_by(user_id=current_user.id).all()
    results = [{'train_id': booking.train_id, 'seat_number': booking.seat_number, 'timestamp': booking.timestamp} for booking in bookings]
    return jsonify(results)

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
