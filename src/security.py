from uuid import uuid4
from user import User
from werkzeug.security import safe_str_cmp

def authenticate(username, password):
    user = User.findByUsername(username)
    if(user!=None and safe_str_cmp(user.password, password)):
        return user

# this method will be integrated with Flask JWT
def identity(payload):
    userId = payload["identity"]
    return User.findById(userId)