import json
from datetime import timedelta
from db import db
from flask import Flask, session, request, render_template, redirect, url_for
from flask_restful import Api
from flask_jwt import JWT
from manager_security import authenticate, identity
from resources.manager_auto import ManagerAutoScale, start_observing
from resources.manager_data import ManagerData
from resources.manager_manual import ManagerManual
from resources.manager_metric import ManagerMetric


# Application initialization and configs.
# Flask is initialized for this application.
# Flask-SQLAlchemy uses MySQL server, and uses 'db' as backing database.
# Flask-JWT tokens have expiration time of one day.
# TEST: MySQL Server Public Connection
# ap.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://ece1779:secret@54.227.216.190/db'
def create_app():
    ap = Flask(__name__)
    ap.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://ece1779:secret@172.31.35.50/db'
    ap.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    ap.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=86400)
    ap.secret_key = 'An_App_Secret_Key'
    db.init_app(ap)
    with ap.app_context():
        db.create_all()
    start_observing(ap.app_context())
    return ap


# Flask-JWT authorization, which by default register the route
# '/auth' for user authentication.
app = create_app()
api = Api(app)
jwt = JWT(app, authenticate, identity)


# Web site endpoints:
# '/' for index (welcome page).
# '/home' for user home page.
# '/login' for user login.
# '/logout' for user logout.
@app.route('/')
def index():
    return render_template('manager_index.html')


@app.route('/manager_home')
def home():
    if "token" not in session:
        return redirect(url_for('index'))
    return render_template('manager_home.html', messages=json.dumps({"token": session['token']}))


# API endpoints, which are self explaining.
@app.route('/manager_login', methods=['POST'])
def login():
    if request.method == 'POST':
        token = request.form['token']
        session['token'] = token
        return json.dumps({'message': 'ok', 'redirect': '/manager_home?token='+token})


@app.route('/manager_logout')
def logout():
    session.pop('token', None)
    return json.dumps({'message': 'ok', 'redirect': '/'})


api.add_resource(ManagerData, '/api/manager_data')
api.add_resource(ManagerManual, '/api/manager_manual')
api.add_resource(ManagerMetric, '/api/manager_metric')
api.add_resource(ManagerAutoScale, '/api/manager_auto_scale_config')

if __name__ == '__main__':
    app.run()
