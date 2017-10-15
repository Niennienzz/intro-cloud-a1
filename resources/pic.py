from flask import request
from flask_restful import Resource
from flask_jwt import jwt_required
from store.trans import PicTrans
from models.pic_url import PicURLModel


class PicUploader(Resource):

    # TODO: Auth and user ID.
    def post(self):
        # read image file
        f = request.files['file']

        # make transforms of image
        pic_trans = PicTrans(f.stream.read())
        (origin, thum, tran1, tran2, tran3) = pic_trans.trans_save()

        # update database
        pic_url = PicURLModel(1, origin, thum, tran1, tran2, tran3)
        pic_url.save_to_db()

        return {'message': 'file uploaded successfully'}
