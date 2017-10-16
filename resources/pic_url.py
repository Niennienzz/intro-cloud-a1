from flask import request
from flask_restful import Resource
from flask_jwt import jwt_required, current_identity
from store.trans import PicTrans
from models.pic_url import PicURLModel


class PicURLResource(Resource):

    @jwt_required()
    def post(self):
        # read image file
        f = request.files['file']

        # make transforms of image
        pic_trans = PicTrans(f.stream.read())
        (origin, thum, tran1, tran2, tran3) = pic_trans.trans_save()

        # update database
        pic_url = PicURLModel(current_identity.id, origin, thum, tran1, tran2, tran3)
        pic_url.save_to_db()

        return {'message': 'file uploaded successfully'}

    @jwt_required()
    def get(self, _id):
        if not _id:
            return {'message': 'no id provided'}, 400
        pic_url = PicURLModel.find_by_id(_id)
        if pic_url:
            return pic_url.json()
        return {'message': 'image not found'}, 404

    @jwt_required()
    def delete(self, _id):
        if not _id:
            return {'message': 'no id provided'}, 400
        pic_url = PicURLModel.find_by_id(_id)
        if pic_url:
            pic_url.delete_from_db()
        return {'message': 'image deleted'}, 404


class PicURLListResource(Resource):

    @jwt_required()
    def get(self):
        return {'data': list(map(lambda x: x.json(), PicURLModel.find_by_user_id(current_identity.id)))}
