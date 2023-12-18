import settings

def db_url() -> str:
    return  '{}://{}:{}@{}:{}/{}'.format(
        settings.FASTAPI_DATABASE.get('MIDDLWARE'),
        settings.FASTAPI_DATABASE.get('USER'),
        settings.FASTAPI_DATABASE.get('PASSWORD'),
        settings.FASTAPI_DATABASE.get('HOST'),
        settings.FASTAPI_DATABASE.get('PORT'),
        settings.FASTAPI_DATABASE.get('NAME')
    )
