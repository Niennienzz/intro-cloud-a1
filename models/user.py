import random
import hashlib

from db import db
from models.const import ALPHABET

class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64))
    password = db.Column(db.String(64))
    pwdsalt = db.Column(db.String(16))

    def __init__(self, username, password):
        self.username = username
        self.pwdsalt = ''.join(random.choice(ALPHABET) for i in range(16))
        self.password = hashlib.sha256((password+self.pwdsalt).encode('utf-8')).hexdigest()
    
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()