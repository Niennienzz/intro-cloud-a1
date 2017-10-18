from datetime import timedelta

from flask import Flask, render_template
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from resources.user import UserRegister
from resources.pic import PicResource
from resources.pic_url import PicURLResource, PicURLListResource
from resources.test import TestUploadResource

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=86400)
app.secret_key = 'An_App_Secret_Key'
api = Api(app)


@app.before_first_request
def create_tables():
    db.create_all()


# Authorization
jwt = JWT(app, authenticate, identity)


# Web Site Endpoints
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/home')
def home():
    return render_template('home.html')


# API Endpoints
api.add_resource(UserRegister, '/user')
api.add_resource(PicURLResource, '/api/pic', '/api/pic/<int:_id>')
api.add_resource(PicURLListResource, '/api/pics')
api.add_resource(PicResource, '/api/image/<path:file_path>')


# Test API Endpoint
api.add_resource(TestUploadResource, '/test/FileUpload')

if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(host='0.0.0.0', port=5000, debug=True)
