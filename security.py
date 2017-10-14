from hashlib import sha256
from werkzeug.security import safe_str_cmp
from models.user import UserModel


def authenticate(username, password):
    user = UserModel.find_by_username(username)
    if user:
        password_hash = sha256((password+user.pwdsalt).encode('utf-8')).hexdigest()
        if safe_str_cmp(password_hash.encode('utf-8'), user.password.encode('utf-8')):
            return user


def identity(payload):
    user_id = payload['identity']
    return UserModel.find_by_id(user_id)
