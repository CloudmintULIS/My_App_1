import re
from werkzeug.security import generate_password_hash, check_password_hash

def validate_username(username):
    return bool(re.match(r'^[a-zA-Z0-9_]{1,30}$', username))

def hash_password(password):
    return generate_password_hash(password)

def verify_password(hash_pw, password):
    return check_password_hash(hash_pw, password)
