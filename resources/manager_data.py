import boto3
import botocore
from const.const import Constants
from flask_restful import Resource
from flask_jwt import jwt_required, current_identity
from models.pic_url import PicURLModel
from models.user import UserModel


class ManagerData(Resource):
    """ManagerData provides API for manager to access user data.
        In our case, it provides only the DELETE method to purge AWS S3 storage and database.
    """
    @jwt_required()
    def delete(self):
        """Delete user data. (DELETE)

        This method purges all user data in AWS S3 storage and database for the application.
        It keeps only the manager account in database.

        Returns:
            (JSON): Data purge success or fail message.
            (int): HTTP status code.
        """
        # special treat for manager
        if current_identity.id != Constants.MANAGER_DATABASE_ID:
            return {'message': 'you are not manager'}, 403

        # get all picture urls
        bucket_name = 'zhehui-ece1779-bucket'
        s3 = boto3.resource('s3')
        bucket = s3.Bucket(bucket_name)
        bucket.objects.all().delete()

        # delete table entries for picurls
        pic_url_models = PicURLModel.get_all()
        for pic_url_model in pic_url_models:
            pic_url_model.delete_from_db()

        # delete table entries for users, keep manager
        users = UserModel.get_all()
        for user in users:
            if user.id == Constants.MANAGER_DATABASE_ID:
                continue
            user.delete_from_db()

        return {'message': 'data purged successfully'}
