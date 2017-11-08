import json
from datetime import timedelta
from db import db
from flask import Flask, session, request, render_template, redirect, url_for
from flask_restful import Api
from flask_jwt import JWT
from security import authenticate, identity
from resources.user import UserRegister
from resources.pic import PicResource
from resources.pic_url import PicUploaderResource, PicURLListResource
from resources.test import TestUploadResource


# Application initialization and configs.
# Flask is initialized for this application.
# Flask-SQLAlchemy uses MySQL server, and uses 'sys' as backing database.
# Flask-JWT tokens have expiration time of one day.
#
def create_app():
    ap = Flask(__name__)
    ap.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost/sys'
    ap.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    ap.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=86400)
    ap.secret_key = 'An_App_Secret_Key'
    db.init_app(ap)
    with ap.app_context():
        db.create_all()
    return ap


# Flask-JWT authorization, which by default register the route
# '/auth' for user authentication.
app = create_app()
api = Api(app)
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


# API endpoints, which are self explaining.
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


api.add_resource(UserRegister, '/api/user_register')
api.add_resource(PicUploaderResource, '/api/pic_upload')
api.add_resource(PicURLListResource, '/api/pic_urls')
api.add_resource(PicResource, '/api/pic/<path:file_path>')

# >>>>> Test API endpoint, which is self explaining.  <<<<<
# >>>>> See /resources/test.py file for more details. <<<<<
api.add_resource(TestUploadResource, '/test/FileUpload')

if __name__ == '__main__':
    app.run()
