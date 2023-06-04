from werkzeug.security import generate_password_hash, check_password_hash


def get_hashed_password(password):
    return generate_password_hash(password=password)

def validate_password_hash(password, hashed_password):
    return check_password_hash(hashed_password, password=password)