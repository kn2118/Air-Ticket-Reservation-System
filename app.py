from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Creating Flask Application 
app = Flask("AirTicketSys")
app.debug = True 

# Connecting Flask to database
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://username:your_password@localhost/air_ticket_reservation_system'

# Define routes 
@app.route('/')
@app.route('/index')

def index():
    return "hello world"

