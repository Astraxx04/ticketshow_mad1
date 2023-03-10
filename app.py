from flask import *
from flask_sqlalchemy import SQLAlchemy
import datetime

app = Flask(__name__, template_folder='templates')
app.secret_key = 'super secret key'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ticket_show.db'

db = SQLAlchemy(app)

class Admins(db.Model):
    admin_id = db.Column(db.Integer(), primary_key = True)
    password = db.Column(db.String(20), nullable = False)

    def __repr__(self):
        return "<Admin %r>" % self.admin_id

class Users(db.Model):
    user_id = db.Column(db.Integer(), primary_key = True)
    password = db.Column(db.String(20), nullable = False)
    usr_name = db.Column(db.String(30), nullable = False)

    def __repr__(self):
        return "<User %r>" % self.user_id

class Venues(db.Model):
    venue_id = db.Column(db.Integer(), primary_key = True)
    venue_name = db.Column(db.String(50), nullable = False)
    venue_place = db.Column(db.String(50), nullable = False)
    venue_location = db.Column(db.String(50), nullable = False)
    venue_capacity = db.Column(db.Integer(), nullable = False)
    shows = db.relationship("Shows")

    def __repr__(self):
        return "<Venue %r>" % self.venue_id

class Shows(db.Model):
    show_id = db.Column(db.Integer(), primary_key = True)
    show_name = db.Column(db.String(50), nullable = False)
    show_time = db.Column(db.DateTime(), nullable = False)
    show_tag = db.Column(db.String(50), nullable = False)
    show_rating = db.Column(db.Integer(), nullable = False)
    show_price = db.Column(db.Integer(), nullable = False)
    svenue_id = db.Column(db.Integer(), db.ForeignKey('venues.venue_id'))

    def __repr__(self):
        return "<Shows %r>" % self.show_id

class Bookings(db.Model):
    booking_id = db.Column(db.Integer(), primary_key = True)
    buser_id = db.Column(db.Integer(), db.ForeignKey('users.user_id'))
    bvenue_id = db.Column(db.Integer(), db.ForeignKey('venues.venue_id'))
    bshow_id = db.Column(db.Integer(), db.ForeignKey('shows.show_id'))
    num_tickets = db.Column(db.Integer(), nullable = False)
    total_price = db.Column(db.Integer(), nullable = False)

    def __repr__(self):
        return "<Bookings %r%r%r>" % self.venue_id % self.show_id % self.booking_id




@app.route('/registeration', methods =["GET", "POST"])
def user_registeration():
    if request.method == 'POST' :
        user_name = request.form.get('username')
        user_password = request.form.get('userpassword')
        user_passwordconf = request.form.get('userpasswordconf')
        if user_password == user_passwordconf:
            reg = Users(password=user_password, usr_name=user_name)
            db.session.add(reg)
            db.session.commit()
            print(user_name, user_password)
            return "user registered"
    return render_template('registeration.html')



@app.route('/newshow', methods =["GET", "POST"])
def new_show():
    if request.method == 'POST' :
        new_showname = request.form.get('new_showname')
        new_showratings = request.form.get('new_showratings')
        new_showtime = request.form.get('new_showtime')
        new_showtag = request.form.get('new_showtag')
        new_showprice = request.form.get('new_showprice')
        print(new_showtime)
        # show = Shows(show_name=new_showname, show_tag=new_showtag, show_rating=new_showratings, show_price=new_showprice, svenue_id=1)
        # db.session.add(show)
        # db.session.commit()
        # print(new_showname, new_showratings, new_showtime, new_showtag, new_showprice)
        return "show registered"
    return render_template('new_show.html')



@app.route('/newvenue', methods =["GET", "POST"])
def new_venue():
    if request.method == 'POST' :
        new_venuename = request.form.get('new_venuename')
        new_venueloc = request.form.get('new_venueloc')
        new_venueplace = request.form.get('new_venueplace')
        new_venuecap = request.form.get('new_venuecap')
        venue = Venues(venue_name=new_venuename, venue_place=new_venueplace, venue_location=new_venueloc, venue_capacity=new_venuecap)
        db.session.add(show)
        db.session.commit()
        print(new_venuename, new_venueloc, new_venueplace, new_venuecap)
        return "venue registered"
    return render_template('new_venue.html')



print(datetime.datetime.utcnow)







@app.route("/")
def index():
    return render_template("admin_login.html")

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        app.run(debug=True)
