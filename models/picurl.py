from db import db
from models.user import UserModel

class PicurlModel(db.Model):
    __tablename__ = 'picurls'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(UserModel.id))
    origin = db.Column(db.String(100))
    suffix_thumb = db.Column(db.String(25))
    suffix_trans1 = db.Column(db.String(25))
    suffix_trans2 = db.Column(db.String(25))
    suffix_trans3 = db.Column(db.String(25))

    user = db.relationship('UserModel', foreign_keys='PicurlModel.user_id', lazy='joined')

    def __init__(self, user_id, origin, thumb, t1, t2, t3):
        self.user_id = user_id
        self.origin = origin
        self.suffix_thumb = thumb
        self.suffix_trans1 = t1
        self.suffix_trans2 = t2
        self.suffix_trans3 = t3

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_user_id(cls, _id):
        return cls.query.filter_by(user_id=_id)