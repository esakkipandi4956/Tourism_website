from flask import Flask, render_template
from flask_mail import Mail
from flask_mysqldb import MySQL
from config import Config

# App setup
app = Flask(__name__)
app.config.from_object(Config)

from db import mysql
mysql.init_app(app)


# Auth DB and Mail
mysql = MySQL(app)
mail = Mail(app)


# Inject into blueprints
from auth.routes import auth_bp
from booking.routes import booking_bp
from cab.routes import cab_bp

app.register_blueprint(auth_bp)
app.register_blueprint(booking_bp)
app.register_blueprint(cab_bp, url_prefix='/cab')

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/places')
def places():
    return render_template('places.html')

@app.route('/hotels')
def hotels():
    return render_template('hotels.html')

@app.route('/gallery')
def gallery():
    return render_template('gallery.html')

@app.route('/blog')
def blog():
    return render_template('blog.html')

@app.route('/service')
def service():
    return render_template('service.html')

@app.route('/contactus')
def contactus():
    return render_template('contactus.html')

@app.route('/blog_details')
def blog_details():
    return render_template('blog_details.html')


# Places

@app.route('/zoo')
def zoo():
    return render_template('zoo.html')

@app.route('/temples')
def temples():
    return render_template('temples.html')

@app.route('/mountains')
def mountains():
    return render_template('mountains.html')

@app.route('/beach')
def beach():
    return render_template('beach.html')

@app.route('/waterfalls')
def waterfalls():
    return render_template('waterfalls.html')

@app.route('/city')
def city():
    return render_template('city.html')

if __name__ == '__main__':
    app.run(debug=True)
