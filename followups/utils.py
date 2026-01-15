import secrets
import string

def generate_code(length=8):
    chars = string.ascii_uppercase + string.digits
    return ''.join(secrets.choice(chars) for _ in range(length))

def generate_token(length=32):
    return secrets.token_urlsafe(length)[:length]