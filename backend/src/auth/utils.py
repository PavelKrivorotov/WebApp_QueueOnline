from uuid import uuid4
import secrets

from passlib.context import CryptContext

import settings

password_context = CryptContext(
    schemes = settings.FASTAPI_CRYPTOGRAPHY_PASSWORD_SCHEMES
)


def make_hash_password(password: str) -> str:
    return '{}-hash'.format(password)

def check_hash_password(password: str, hash_password: str) -> bool:
    if (make_hash_password(password) == hash_password): return True
    return False

def make_token() -> str:
    return 'Token: {}'.format(str(uuid4()))




def hash_password(raw_password: str) -> str:
    return password_context.hash(raw_password)

def check_password(raw_password: str, hash_password: str) -> bool:
    return password_context.verify(raw_password, hash_password)


def generate_token() -> str:
    return secrets.token_hex(settings.FASTAPI_AUTHORIZATION_TOKEN_LENGTH)
