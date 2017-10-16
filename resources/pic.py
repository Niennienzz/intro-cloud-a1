from flask import make_response
from flask_restful import Resource
from store.trans import PicStore


class PicResource(Resource):

    def get(self, file_path):
        if not file_path:
            return {'message': 'no image path provided'}, 400
        if file_path.startswith('images/'):
            file_path = file_path[len('images/'):]
        pic_store = PicStore(file_path, None)
        data, ok = pic_store.get()
        if not ok:
            return {'message': 'no image found'}, 404
        response = make_response(data)
        response.headers['content-type'] = 'image/jpeg'
        return response

