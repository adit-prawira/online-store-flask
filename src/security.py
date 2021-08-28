from uuid import uuid4
from user import User
from werkzeug.security import safe_str_cmp
id = str(uuid4())
users = [
    User(id, "adityaaaap",  "aditp956", "Aditya", "Prawira")
]

usernameMapping = {u.username: u for u in users} # use set comprehension
userIdMapping = {u.id: u for u in users}

def authenticate(username, password):
    user = usernameMapping.get(username, None)
    if(user!=None and safe_str_cmp(user.password, password)):
        return user

# this method will be integrated with Flask JWT
def identity(payload):
    userId = payload["identity"]
    return userIdMapping.get(userId, None)