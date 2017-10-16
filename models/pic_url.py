from db import db
from models.user import UserModel


class PicURLModel(db.Model):

    __tablename__ = 'picurls'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(UserModel.id))
    origin = db.Column(db.String(100))
    thumb = db.Column(db.String(100))
    trans1 = db.Column(db.String(100))
    trans2 = db.Column(db.String(100))
    trans3 = db.Column(db.String(100))

    user = db.relationship('UserModel', foreign_keys='PicURLModel.user_id', lazy='joined')

    def __init__(self, user_id, origin, thumb, t1, t2, t3):
        self.user_id = user_id
        self.origin = origin
        self.thumb = thumb
        self.trans1 = t1
        self.trans2 = t2
        self.trans3 = t3

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def json(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'origin_url': self.origin,
            'thumb_url': self.thumb,
            'trans1_url': self.trans1,
            'trans2_url': self.trans2,
            'trans3_url': self.trans3
        }

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_by_user_id(cls, _id):
        return cls.query.filter_by(user_id=_id)
