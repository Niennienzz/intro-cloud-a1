import asyncio
from const.const import Constants
from flask_restful import Resource
from flask_jwt import jwt_required, current_identity
from models.pic_url import PicURLModel
from models.user import UserModel
from store.s3 import PicS3Store


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
        pic_url_models = PicURLModel.get_all_full()
        urls = []
        for pic_url_model in pic_url_models:
            urls.append(pic_url_model.origin)
            urls.append(pic_url_model.thumb)
            urls.append(pic_url_model.trans1)
            urls.append(pic_url_model.trans2)
            urls.append(pic_url_model.trans3)

        # make s3 store objects
        s3_stores = []
        for url in urls:
            s3_stores.append(PicS3Store(url, None))

        # get delete funcs
        s3_delete_funcs = []
        for store in s3_stores:
            s3_delete_funcs.append(store.delete)

        # run each delete func in a coroutine
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(asyncio.gather(
            *(func() for func in s3_delete_funcs)
        ))
        loop.close()

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
