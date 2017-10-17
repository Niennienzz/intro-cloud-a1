from flask import request
from flask_restful import Resource
from store.trans import PicTrans
from models.pic_url import PicURLModel
from models.user import UserModel


class TestUploadResource(Resource):

    def post(self):
        form = request.form
        username = form['field1']
        password = form['field2']
        f = request.files['field3']

        user = UserModel.find_by_username(username)
        if user:
            user_id = user.id
        else:
            new_user = UserModel(username, password)
            new_user.save_to_db()
            user_id = UserModel.find_by_username(username).id

        # make transforms of image
        pic_trans = PicTrans(f.stream.read())
        origin = pic_trans.trans_save()

        # update database
        pic_url = PicURLModel(user_id, origin)
        pic_url.save_to_db()

        return {'message': 'user created/validated, file uploaded successfully'}

