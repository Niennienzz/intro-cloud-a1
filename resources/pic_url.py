from flask import request
from flask_restful import Resource
from flask_jwt import jwt_required, current_identity
from store.trans import PicTrans
from models.pic_url import PicURLModel


class PicUploaderResource(Resource):
    """PicUploaderResource provides image upload API.
    """

    @jwt_required()
    def post(self):
        """Upload an image. (POST)

        This method requires user authentication via JWT.
        It generate transformations of the original image and save them on disk.
        It then updates the image URL database table.

        Returns:
            (JSON): Image success or fail message.
            (int): HTTP status code, 200 for Success, 400 for Bad Request, and 500 for Server Internal Error.
        """
        # read image file
        f = request.files['file']
        if f is None:
            return {'message': 'no file chosen'}, 400

        try:
            # make transforms of image
            pic_trans = PicTrans(f.stream.read())
            origin = pic_trans.trans_save()

            # update database
            pic_url = PicURLModel(current_identity.id, origin)
            pic_url.save_to_db()
        except IOError:
            return {'message': 'internal server error'}, 500

        return {'message': 'file uploaded successfully'}


class PicURLListResource(Resource):
    """PicURLListResource provides access to a user's image URL list.
    """

    @jwt_required()
    def get(self):
        """Retrieve image URL list. (GET)

        This method requires user authentication via JWT.

        Returns:
            (JSON): image URL list.
            (int): HTTP status code, 200 for Success.
        """
        return {'pic_urls': list(map(lambda x: x.json(), PicURLModel.find_by_user_id(current_identity.id)))}
