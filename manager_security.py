from hashlib import sha256
from werkzeug.security import safe_str_cmp
from models.user import UserModel


def authenticate(username, password):
    """User authentication.

    This function a Flask-JWT authentication_handler.
    It compares the username and password in database.
    Note that user password is stored as SHA-256 hash with a user specific salt.
    The function generates the hash again and compares with the stored hash.

    Args:
        username (str): Username of an account.
        password (str): Password of an account.

    Returns:
        (UserModel): The user account if auth is successful, otherwise None.
    """
    if username == 'admin' and password == 'admin':
        manager = UserModel.find_by_username(username)
        if manager:
            password_hash = sha256((password + manager.pwdsalt).encode('utf-8')).hexdigest()
            if safe_str_cmp(password_hash.encode('utf-8'), manager.password.encode('utf-8')):
                return manager


def identity(payload):
    """User identity.

    This function a Flask-JWT identity_handler.
    It retrieves the user account from payload.

    Args:
        payload: The JWT payload.

    Returns:
        (UserModel): The user account.
    """
    manager_id = payload['identity']
    return UserModel.find_by_id(manager_id)
