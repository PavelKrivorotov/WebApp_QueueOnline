from typing import Annotated

from fastapi import HTTPException, Header, Depends, status
from sqlalchemy.orm import Session

import settings
from database import db_connection

from .base import BaseAuthCRUD
from .models import User, Token
from .schemes import UserRetrieveSchemeOUT


class BaseAuthDepends:
    _role: str = None
    _db_field: str = None

    user: User = None
    token: Token = None

    def __init__(
            self,
            token: Annotated[str, Header()] = None,
            db: Session = Depends(db_connection)
        ) -> None:

        self._db = db
        self.token = self.verify_role_token(token)

    def verify_role_token(self, token: str) -> Token | None:
        if (self._role == settings.FASTAPI_DEFAULT_PERMISSION_DEPENDENCIES):
            return None

        token = BaseAuthCRUD._retrieve_token(self._db, token)
        if (token is None):
            raise HTTPException(
                status_code = status.HTTP_401_UNAUTHORIZED,
                detail = 'Invalid token ({})'.format(token)
            )

        self._check_user_role(token)
        return token

    def _check_user_role(self, token: Token) -> None:        
        # if token.user_id is None?
        user  = self._db.get(User, token.user_id)
        self.user = user

        user_schema = UserRetrieveSchemeOUT.model_validate(user).model_dump()
        if (user_schema[self._db_field] is False):
            raise HTTPException(
                status_code = 403,
                detail = 'Permission denied! Allowed ({}) role!'.format(self._role)
            )


class AllowAny(BaseAuthDepends):
    _role = 'AllowAny'

class IsAuthenticated(BaseAuthDepends):
    _role = 'IsAuthenticated'
    _db_field = 'is_active'

class IsSuperuser(BaseAuthDepends):
    _role = 'IsSuperuser'
    _db_field = 'is_superuser'
