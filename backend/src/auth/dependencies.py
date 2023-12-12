from typing import Annotated

from fastapi import HTTPException, Header, Depends, status
from sqlalchemy.orm import Session

import settings
from database import db_connection

from .base import BaseAuthCRUD
from .models import User
from .schemes import UserRetrieveSchemeOUT


class BaseAuthDepends:
    _role: str = None
    _db_field: str = None

    user: User = None

    def __init__(
            self,
            token: Annotated[str, Header()] = None,
            db: Session = Depends(db_connection)
        ) -> None:

        self._db = db
        self.token = self.verify_role_token(token)

    def verify_role_token(self, token: str):
        if (self._role == settings.FASTAPI_DEFAULT_PERMISSION_DEPENDENCIES):
            return token

        self._check_user_role(token)
        return token

    def _check_user_role(self, token: str) -> None:
        user = BaseAuthCRUD.get_user_by_token(self._db, token)
        if (user is None):
            raise HTTPException(
                status_code = status.HTTP_401_UNAUTHORIZED,
                detail = 'Invalid token ({})'.format(token)
            )
        
        # 
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
