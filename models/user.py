from random import choice
from hashlib import sha256
from db import db
from const.const import Constants


class UserModel(db.Model):
    """UserModel provides user data model ORM.

        It saves username, password, and password salt for a user account in database.
        It provides filter-by-username and filter-by-userID helpers.

        Schema:
            CREATE TABLE users (
                id INTEGER NOT NULL,
                username VARCHAR(64),
                password VARCHAR(64),
                pwdsalt VARCHAR(16),
                PRIMARY KEY (id)
            )
    """

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64))
    password = db.Column(db.String(64))
    pwdsalt = db.Column(db.String(16))

    def __init__(self, username, password):
        self.username = username
        self.pwdsalt = ''.join(choice(Constants.ALPHABET) for i in range(16))
        self.password = sha256((password+self.pwdsalt).encode('utf-8')).hexdigest()
    
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
