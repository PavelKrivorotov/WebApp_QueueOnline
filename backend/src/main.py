from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

import settings

from auth.routers import router as auth_router
from turn.routers import router as chat_router


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.FASTAPI_MIDDLWEARE_ALLOWED_ORIGINS,
    allow_credentials=settings.FASTAPI_MIDDLWARE_ALLOWED_CREDENTIALS,
    allow_methods=settings.FASTAPI_MIDDLWARE_ALLOWED_METHODS,
    allow_headers=settings.FASTAPI_MIDDLWARE_ALLOWED_HEADERS,
)

app.include_router(auth_router)
app.include_router(chat_router)


if __name__ == '__main__':
    # For local (host="127.0.0.1", port=8000)
    # ...

    # For docker (host="0.0.0.0", port=8000)
    uvicorn.run(
        'main:app',
        host = settings.FASTAPI_HOST,
        port = settings.FASTAPI_PORT,
        log_level = settings.FASTAPI_LOG_LEVEL
    )
