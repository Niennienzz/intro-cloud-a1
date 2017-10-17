from os import path
from db import db
from models.user import UserModel
from const.const import Constants


class PicURLModel(db.Model):

    __tablename__ = 'picurls'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(UserModel.id))
    origin = db.Column(db.String(100))

    user = db.relationship('UserModel', foreign_keys='PicURLModel.user_id', lazy='joined')

    def __init__(self, user_id, origin):
        self.user_id = user_id
        self.origin = origin
        self.thumb = path.join(path.dirname(self.origin), Constants.THUMB)
        self.trans1 = path.join(path.dirname(self.origin), Constants.TRANS_1)
        self.trans2 = path.join(path.dirname(self.origin), Constants.TRANS_2)
        self.trans3 = path.join(path.dirname(self.origin), Constants.TRANS_3)

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
        row = cls.query.filter_by(id=_id).first()
        result = PicURLModel(row.user_id, row.origin)
        result.id = row.id
        return result

    @classmethod
    def find_by_user_id(cls, _id):
        results = []
        rows = cls.query.filter_by(user_id=_id).order_by(PicURLModel.id)
        for row in rows:
            result = PicURLModel(row.user_id, row.origin)
            result.id = row.id
            results.append(result)
        return results
