from flask_restful import Resource, reqparse
from models.user import UserModel


class UserRegister(Resource):
    """UserRegister provides user registration API.

        Attributes:
            parser (RequestParser): The Flask-RESTful request parser.
            It parses username and password from the JSON payload during user registration.
    """
    parser = reqparse.RequestParser()
    parser.add_argument(
        'username',
        type=str,
        required=True
    )

    parser.add_argument(
        'password',
        type=str,
        required=True
    )

    def post(self):
        """Register a user. (POST)

        This method checks if a user account already exists.
        If so, the registration will be aborted.
        Else, a user account will be save to database.

        Returns:
            (JSON): Registration success or fail message.
            (int): HTTP status code, 201 for Created and 400 for Bad Request.
        """
        data = UserRegister.parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {'message': 'user already exists'}, 400

        user = UserModel(data['username'], data['password'])
        user.save_to_db()

        return {'message': 'user created successfully'}, 201
