from flask_restful import Resource, reqparse
from flask_jwt import jwt_required, current_identity
from models.user import UserModel


class UserRegister(Resource):

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

    @jwt_required()
    def get(self):
        return {'message': 'user found'}

    def post(self):
        data = UserRegister.parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {'message': 'user already exists'}, 400

        user = UserModel(data['username'], data['password'])
        user.save_to_db()

        return {'message': 'user created successfully'}, 201
