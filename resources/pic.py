from flask import make_response
from flask_restful import Resource
from store.trans import PicStore


class PicResource(Resource):
    """PicResource provides image data access API.
    """

    def get(self, file_path):
        """Retrieve an image data. (GET)

        This method checks if a filepath is provided.
        If so, it strips prefix 'images/' which is the API agreed on client and server.
        It then looks the file using the rest of the filepath via storage classes.

        Returns:
            (bytes): Image data in binary.
            (int): HTTP status code, 200 for Success, 400 for Bad Request, and 404 for Not Found.
        """
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

