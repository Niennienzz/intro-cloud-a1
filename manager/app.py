import json
from datetime import timedelta
from flask import Flask, session, request, render_template, redirect, url_for
from flask_restful import Api
from flask_jwt import JWT
from manager.db import db
from manager.security import authenticate, identity


""" Application initialization and configs.

Flask is initialized for this application.
Flask-SQLAlchemy uses MySQL server, and uses 'sys' as backing database.
Flask-JWT tokens have expiration time of one day.
"""
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost/sys'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=86400)
app.secret_key = 'An_Manager_Secret_Key'
api = Api(app)


# Ensure database tables are created.
@app.before_first_request
def create_tables():
    db.create_all()


# Flask-JWT authorization, which by default register the route
# '/auth' for user authentication.
jwt = JWT(app, authenticate, identity)


# Web site endpoints:
# '/' for index (welcome page).
# '/home' for user home page.
# 'login' for user login.
# 'logout' for user logout.
@app.route('/')
def index():
    return render_template('manager_index.html')

