# Middlware section
FASTAPI_MIDDLWEARE_ALLOWED_ORIGINS = [
    'http://localhost:5173',
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
FASTAPI_DATABASE_SETTINGS = {
    'MIDDLWARE': 'postgresql',
    'USER':      'postgres',
    'PASSWORD':  'postgres',
    'NAME':      'task_15_11_2023',
    'HOST':      '127.0.0.1',
    'PORT':      5432,
}

FASTAPI_DATABASE_URL = '{}://{}:{}@{}:{}/{}'.format(
    FASTAPI_DATABASE_SETTINGS.get('MIDDLWARE'),
    FASTAPI_DATABASE_SETTINGS.get('USER'),
    FASTAPI_DATABASE_SETTINGS.get('PASSWORD'),
    FASTAPI_DATABASE_SETTINGS.get('HOST'),
    FASTAPI_DATABASE_SETTINGS.get('PORT'),
    FASTAPI_DATABASE_SETTINGS.get('NAME')
)
