from flask import *
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import *
from flask_login import LoginManager, current_user, login_user, logout_user, login_required, UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

app = Flask(__name__, template_folder='templates')
app.secret_key = 'super secret key'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ticket_show.db'
app.config['TESTING'] = False
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.session_protection = 'strong'
login_manager.login_view = 'login'


#Login Manager----------------------------------------------------------------

@login_manager.user_loader
def load_user(user_id):
    # return the user object for the user with the given user_id
    return Users.query.get(int(user_id))


#Models--------------------------------

# class Admins(db.Model, UserMixin):
#     admin_id = db.Column(db.Integer(), primary_key = True)
#     admin_name = db.Column(db.String(30), nullable = False)
#     password = db.Column(db.String(20), nullable = False)

#     def __repr__(self):
#         return "<Admin %r>" % self.admin_id

class Users(db.Model, UserMixin):
    user_id = db.Column(db.Integer(), primary_key = True)
    password = db.Column(db.String(20), nullable = False)
    usr_name = db.Column(db.String(30), nullable = False)
    userType = db.Column(db.String(20), default = 'user')

    def get_id(self):
           return (self.user_id)

    def __repr__(self):
        return "<User %r>" % self.user_id

    def isAdmin(self): 
        if self.userType == 'admin':
            return True
        else:
            return False



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
    show_time = db.Column(db.String(50), nullable = False)
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






#Forms----------------------------------------------------------------

class AdminLoginForm(FlaskForm):
    adminname = StringField('Admin Name', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])


class UserLoginForm(FlaskForm):
    username = StringField('User Name', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])


class UserRegisterationForm(FlaskForm):
    username = StringField('User Name', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    passwordconf = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password', message='Passwords must match!')])


class NewVenueForm(FlaskForm):
    venuename = StringField('Venue Name', validators=[DataRequired()])
    venueplace = StringField('Venue Place', validators=[DataRequired()])
    venueloc = StringField('Venue Location', validators=[DataRequired()])
    venuecap = StringField('Venue Capacity', validators=[DataRequired()])


class NewShowForm(FlaskForm):
    showname = StringField('Show Name', validators=[DataRequired()])
    ratings = StringField('Show Rating', validators=[DataRequired()])
    starttime = StringField('Show Time', validators=[DataRequired()])
    tags = StringField('Show Tag', validators=[DataRequired()])
    price = StringField('Show Price', validators=[DataRequired()])


class NewTicketBookingForm(FlaskForm):
    buser_id = db.Column(db.Integer(), db.ForeignKey('users.user_id'))
    bvenue_id = db.Column(db.Integer(), db.ForeignKey('venues.venue_id'))
    bshow_id = db.Column(db.Integer(), db.ForeignKey('shows.show_id'))
    numseats = StringField('Number of Tickets', validators=[DataRequired()])
    price = StringField('Price', validators=[DataRequired()])    
    total = StringField('Total Price', validators=[DataRequired()])



#Routes--------------------------------------------------------------


@app.route("/")
def index():
    return render_template("welcome.html")



@app.route('/adminlogin', methods =["GET", "POST"])
def adminlogin():
    form = AdminLoginForm()

    if form.validate_on_submit():
        user = Users.query.filter_by(usr_name=form.adminname.data).first()
        if user and Users.isAdmin(user):
            if user.password == form.password.data:
                login_user(user)
                return redirect(url_for('admindashboard'))
            else:
                return '<h1>Invalid Password</h1>'


    return render_template('admin_login.html', title='Admin Login', form=form)



@app.route('/userlogin', methods =["GET", "POST"])
def login():
    form = UserLoginForm()

    if form.validate_on_submit():
        user = Users.query.filter_by(usr_name=form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('userdashboard'))
            else:
                return '<h1>Invalid Password</h1>'
    return render_template('user_login.html', title='User Login', form=form)



@app.route('/registeration', methods =["GET", "POST"])
def user_registeration():
    form = UserRegisterationForm()

    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        user = Users(password=hashed_password, usr_name=form.username.data)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return redirect(url_for('userlogin'))
    return render_template('registeration.html', title='Registeration', form=form)



@app.route('/userdashboard', methods =["GET", "POST"])
@login_required
def userdashboard():
    return render_template('user_dashboard.html', title='User Dashboard')



@app.route('/admindashboard', methods =["GET", "POST"])
@login_required
def admindashboard():
    venues = Venues.query.all()
    venu=[]
    for ven in venues:
        shows = Shows.query.filter(ven.venue_id==Shows.svenue_id).all()
        show=[]
        for sho in shows:
            print(sho.show_name)
            show.append({"name": sho.show_name, "time": sho.show_time})
        venu.append({"name": ven.venue_name, "cards": show})
    print(venu)

    return render_template('admin_dashboard.html', title='Admin Dashboard', data=venu)



@app.route('/ticketbooking', methods =["GET", "POST"])
@login_required
def ticketbooking():
    form = NewTicketBookingForm()

    if form.validate_on_submit():
        booking = Bookings(num_tickets=form.numseats.data, total_price=form.total.data)
        db.session.add(booking)
        db.session.commit()
        return redirect(url_for('userdashboard'))
    return render_template('ticket_book.html', title='Ticket Booking', form=form)



@app.route('/userbookings', methods =["GET", "POST"])
@login_required
def userbookings():
    return render_template('user_bookings.html')



@app.route('/newshow', methods =["GET", "POST"])
@login_required
def new_show():
    form = NewShowForm()

    if form.validate_on_submit():
        show = Shows(show_name=form.showname.data, show_time=form.starttime.data, show_tag=form.tags.data, show_rating=form.ratings.data, show_price=form.price.data)
        db.session.add(show)
        db.session.commit()
        return redirect(url_for('admindashboard'))
    return render_template('new_show.html', title='New Show', form=form)



@app.route('/newvenue', methods =["GET", "POST"])
@login_required
def new_venue():
    form = NewVenueForm()

    if form.validate_on_submit():
        venue = Venues(venue_name=form.venuename.data, venue_place=form.venueplace.data, venue_location=form.venueloc.data, venue_capacity=form.venuecap.data)
        db.session.add(venue)
        db.session.commit()
        return redirect(url_for('admindashboard'))
    return render_template('new_venue.html', title='New Venue', form=form)



@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))













if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        app.run(debug=True)