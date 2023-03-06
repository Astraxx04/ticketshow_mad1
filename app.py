from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ticket_show.db'

db = SQLAlchemy(app)

class Admins(db.Model):
    admin_id = db.Column(db.Integer(), primary_key = True)
    password = db.Column(db.String(20), nullable = False)

class Users(db.Model):
    user_id = db.Column(db.Integer(), primary_key = True)
    password = db.Column(db.String(20), nullable = False)
    usr_name = db.Column(db.String(30), nullable = False)

class Venues(db.Model):
    venue_id = db.Column(db.Integer(), primary_key = True)
    venue_name = db.Column(db.String(50), nullable = False)

class Shows(db.Model):
    show_id = db.Column(db.Integer(), primary_key = True)
    show_name = db.Column(db.String(50), nullable = False)
    show_time = db.Column(db.DateTime(), nullable = False)
    show_tag = db.Column(db.String(50), nullable = False)
    show_rating = db.Column(db.Integer(), nullable = False)
    show_price = db.Column(db.Integer(), nullable = False)

class Bookings(db.Model):
    booking_id = db.Column(db.Integer(), primary_key = True)
    buser_id = db.Column(db.Integer(), db.ForeignKey('users.user_id'))
    bvenue_id = db.Column(db.Integer(), db.ForeignKey('venues.venue_id'))
    bshow_id = db.Column(db.Integer(), db.ForeignKey('shows.show_id'))
    num_tickets = db.Column(db.Integer(), nullable = False)
    total_price = db.Column(db.Integer(), nullable = False)