import json
from datetime import timedelta
from flask import Flask, session, request, render_template, redirect, url_for
from flask_restful import Api
from flask_jwt import JWT
from security import authenticate, identity
from resources.user import UserRegister
from resources.pic import PicResource
from resources.pic_url import PicURLResource, PicURLListResource
from resources.test import TestUploadResource


""" Application initialization and configs.

Flask is initialized for this application.
Flask-SQLAlchemy uses SQLite3 by default, and uses data.db as backing file.
Flask-JWT tokens have expiration time of one day.
"""
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=86400)
app.secret_key = 'An_App_Secret_Key'
api = Api(app)


# Ensure database tables are created.
@app.before_first_request
def create_tables():
    db.create_all()


# Flask-JWT authorization, which by default register the route '/auth'
jwt = JWT(app, authenticate, identity)


# Web site endpoints:
# '/' for index (welcome page).
# '/home' for user home page.
# 'login' for user login.
# 'logout' for user logout.
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/home')
def home():
    if "token" not in session:
        return redirect(url_for('index'))
    return render_template('home.html', messages=json.dumps({"token": session['token']}))


@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        token = request.form['token']
        session['token'] = token
        return json.dumps({'message': 'ok', 'redirect': '/home?token='+token})


@app.route('/logout')
def logout():
    session.pop('token', None)
    return json.dumps({'message': 'ok', 'redirect': '/'})


# API endpoints, which are self explaining.
api.add_resource(UserRegister, '/user')
api.add_resource(PicURLResource, '/api/pic_url', '/api/pic_url/<int:_id>')
api.add_resource(PicURLListResource, '/api/pic_urls')
api.add_resource(PicResource, '/api/pic/<path:file_path>')


# Test API endpoint, which is self explaining.
api.add_resource(TestUploadResource, '/test/FileUpload')

if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(host='0.0.0.0', port=5000, debug=True)
