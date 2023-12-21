import os
from  pathlib import Path 
import dotenv

# Loading .env variables
BASE_DIR = Path(__file__).parent

dotenv.load_dotenv(
    dotenv_path = Path(BASE_DIR.parent, '.env')
)


# Middlware section
FASTAPI_MIDDLWEARE_ALLOWED_ORIGINS = [
    'http://localhost:5173',

    # Worked with docker
    'http://127.0.0.1'


    # Not ...
    # 'http://127.0.0.1:8000',

    # Not
    # 'http://backend:8000',

    # Not
    # 'http://frontend:8000',

    # Not
    # 'http://127.0.0.1:80',
]

FASTAPI_MIDDLWARE_ALLOWED_CREDENTIALS = True
FASTAPI_MIDDLWARE_ALLOWED_METHODS = ['*']
FASTAPI_MIDDLWARE_ALLOWED_HEADERS = ['*']


# Cryptography section
FASTAPI_CRYPTOGRAPHY_PASSWORD_SCHEMES = [
    'bcrypt',
]


# Token section
FASTAPI_AUTHORIZATION_TOKEN_LENGTH = 64


# Permiddion section
FASTAPI_PERMISSIONS_DEPENDENCIES = [
    'AllowAny',
    'IsAuthenticated',
    'IsSuperuser',
]

FASTAPI_DEFAULT_PERMISSION_DEPENDENCIES = 'AllowAny'


# Database section:
FASTAPI_DATABASE = {
    'MIDDLWARE': os.getenv('FASTAPI_DATABASE_MIDDLWARE'),
    'USER':      os.getenv('FASTAPI_DATABASE_USER'),
    'PASSWORD':  os.getenv('FASTAPI_DATABASE_PASSWORD'),
    'NAME':      os.getenv('FASTAPI_DATABASE_NAME'),
    'HOST':      os.getenv('FASTAPI_DATABASE_HOST'),
    'PORT':      int(os.getenv('FASTAPI_DATABASE_PORT')),
}


# Server ssection
FASTAPI_HOST = os.getenv('FASTAPI_HOST')
FASTAPI_PORT = int(os.getenv('FASTAPI_PORT'))
FASTAPI_LOG_LEVEL = "info"
