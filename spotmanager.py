import os

from flask import Flask, render_templaterender_template, request, redirect, url_for, session, flash, g
from functools import wraps
from flask_sqlalchemy import SQLAlchemy

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "spotdatabase.db"))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file

# app.secret_key = "&"

db = SQLAlchemy(app)

class Spot(db.Model):
    place = db.Column(db.String(80), unique=True, nullable=False, primary_key=True)
    address = db.Column(db.String(80), unique=True, nullable=False)
    phone = db.Column(db.Int, unique=True)
    lat = db.Column(db.Real, nullable=False)
    lon = db.Column(db.Read, nullable=False)
    visited = db.Column(db.INT, unique=True, nullable=False)
    rating = db.Column(db.INT, unique=True, nullable=False)
    tags = db.Column(db.String(80), unique=True, nullable=False)
   
    def __repr__(self):
        return "<Name: {}>".format(self.place)

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
                return f(*args, **kwargs)
        else:
                flash('Please log in.')
                return redirect(url_for('login'))
    return wrap

@app.route("/", methods=["GET", "POST"])
@login_required
def home():
    spots = None
    if request.form:
        try:
            venue = Spot(place=request.form.get("venue")
            # TODO: add stuuf here
            )
            db.session.add(venue)
            db.session.commit()
        except Exception as e:
            print("Failed to add spot")
            print(e)
    spots = Spot.query.all()
    return render_template("index.html", spots=spots)

@app.route("/update", methods=["POST"])
def update():
    try:
        newname = request.form.get("newname")
        oldname = request.form.get("oldname")
        spot = Spot.query.filter_by(place=oldname).first()
        spot.place = newname
        db.session.commit()
    except Exception as e:
            print("Failed to update spot")
            print(e)
    return redirect("/")

# TODO: Add other adjustments
@app.route("/updatea", methods=["POST"])
def updatea():
    try:
            newwriter = request.form.get("newwriter")
            oldwriter = request.form.get("oldwriter")
            book = Book.query.filter_by(writer=oldwriter).first()
            book.writer = newwriter
            db.session.commit()
    except Exception as e:
        print("Couldn't update book author")
        print(e)
    return redirect("/")

@app.route("/delete", methods=["POST"])
def delete():
    place = request.form.get("place")
    spot = Spot.query.filter_by(place=place).first()
    db.session.delete(spot)
    db.session.commit()
    return redirect("/")

@app.route('/welcome')
def welcome():
    return render_template('welcome.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
        else:
            session['logged_in'] = True
            flash('Welcome! You are now logged in.')
            return redirect(url_for('home'))
    return render_template('login.html', error=error)

@app.route('/logout')
@login_required
def logout():
    session.pop('logged_in', None)
    flash('You are now logged out. Thanks for reading!')
    return redirect(url_for('welcome'))
  
if __name__ == "__main__":
    app.run(debug=True)