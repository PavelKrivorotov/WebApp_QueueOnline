from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.responses import JSONResponse, Response
from sqlalchemy.orm import Session

from database import db_connection
from .schemes import (
    UserCreateSchemeIN,
    UserRetrieveSchemeOUT,
    TokenCreateSchemeIN,
    TokenRetrieveSchemeOUT,
)
from .services import auth
from .dependencies import AllowAny, BaseAuthDepends, IsAuthenticated


router = APIRouter()

@router.get('/user/token-confirm', dependencies=[Depends(IsAuthenticated)])
def user_token_confirm() -> Response:
    return Response(
        status_code=status.HTTP_200_OK
    )

@router.post('/user/registrate', dependencies=[Depends(AllowAny)])
def user_registrate(
        data: UserCreateSchemeIN,
        db: Session = Depends(db_connection)
    ) -> JSONResponse:

    user = auth.create(db, data)
    if (user is None):
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = 'This email adress already exists!'
        )

    return JSONResponse(
        content = UserRetrieveSchemeOUT.model_validate(user).model_dump(),
        status_code = status.HTTP_201_CREATED
    )

@router.post('/user/login', dependencies=[Depends(AllowAny)])
def user_login(
        data: TokenCreateSchemeIN,
        db: Session = Depends(db_connection)
) -> JSONResponse:

    token = auth.login(db, data)
    if (token is None):
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = 'Credentials was not provided!'
        )

    return JSONResponse(
        content = TokenRetrieveSchemeOUT.model_validate(token).model_dump(),
        status_code = status.HTTP_202_ACCEPTED
    )

@router.delete('/user/logout')
def user_logout(
        user: BaseAuthDepends = Depends(IsAuthenticated),
        db: Session = Depends(db_connection)
    ) -> JSONResponse:

    result = auth.logout(db, user)
    return Response(
        status_code = status.HTTP_204_NO_CONTENT
    )
