from hashlib import sha256
from werkzeug.security import safe_str_cmp
from models.user import UserModel


def authenticate(username, password):
    """User authentication.

    This function a Flask-JWT authentication_handler.
    It is used to authenticate the admin account for manager UI.
    The username/password are all 'admin'.

    Args:
        username (str): Username of an account.
        password (str): Password of an account.

    Returns:
        (UserModel): The user account if auth is successful, otherwise None.
    """
    user = UserModel.find_by_username(username)
    if user:
        password_hash = sha256((password + user.pwdsalt).encode('utf-8')).hexdigest()
        if safe_str_cmp(password_hash.encode('utf-8'), user.password.encode('utf-8')):
            return user


def identity(payload):
    """User identity.

    This function a Flask-JWT identity_handler.
    It retrieves the user account from payload.

    Args:
        payload: The JWT payload.

    Returns:
        (UserModel): The user account.
    """
    user_id = payload['identity']
    return UserModel.find_by_id(user_id)
