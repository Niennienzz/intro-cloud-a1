from hashlib import sha256
from werkzeug.security import safe_str_cmp
from models.user import UserModel
from flask_jwt import authentication_handler, identity_handler


@authentication_handler
def authenticate(username, password):
    """Authenticate a user.
    
    This function a Flask-JWT authentication_handler.
    It compares the username and password in database.
    Note that user password is stored as SHA-256 hash with a user specific salt.
    The function generates the hash again and compares with the stored hash.

    Args:
        username (str): Username of an account.
        password (str): Password of an account.
    
    Returns:
        UserModel: The user account if auth is successful, otherwise None.
    """
    user = UserModel.find_by_username(username)
    if user:
        password_hash = sha256((password+user.pwdsalt).encode('utf-8')).hexdigest()
        if safe_str_cmp(password_hash.encode('utf-8'), user.password.encode('utf-8')):
            return user

        
@identity_handler
def identity(payload):
    """Authenticate a user.
    
    This function a Flask-JWT identity_handler.
    It retrieves the user account from payload.

    Args:
        payload: The JWT payload.
    
    Returns:
        UserModel: The user account.
    """
    user_id = payload['identity']
    return UserModel.find_by_id(user_id)
