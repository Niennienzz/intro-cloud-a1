from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from resources.user import UserRegister
from resources.pic import PicUploader

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'An_App_Secret_Key'
api = Api(app)

@app.before_first_request
def create_tables():
    db.create_all()

# Authorization
jwt = JWT(app, authenticate, identity)

# API Endpoints
api.add_resource(UserRegister, '/user')
api.add_resource(PicUploader, '/api/uploader')

if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)