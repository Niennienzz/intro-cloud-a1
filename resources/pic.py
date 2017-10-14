from flask import request
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required, current_identity
from werkzeug import secure_filename
from store.pictore import PicStore
from models.picurl import PicurlModel


class PicUploader(Resource):

    # TODO: Auth and user ID.
    def post(self):
        f = request.files['file']

        pic_store = PicStore(secure_filename(f.filename), f.stream.read())
        (path, ok) = pic_store.save()

        pic_url = PicurlModel(1, path, '', '', '', '')
        pic_url.save_to_db()

        return {'message': 'file uploaded successfully'}
