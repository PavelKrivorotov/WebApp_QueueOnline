from fastapi import Body
from pydantic import BaseModel, ConfigDict


class UserScheme(BaseModel):
    email: str = Body()
    first_name: str | None = Body()
    last_name: str | None = Body()

class UserCreateSchemeIN(UserScheme):
    password: str = Body()

class UserRetrieveSchemeOUT(UserScheme):
    model_config = ConfigDict(from_attributes=True)

    is_active: bool
    is_superuser: bool

class UserListSchemeOUT(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    users: list[UserRetrieveSchemeOUT]


class TokenCreateSchemeIN(BaseModel):
    email: str = Body()
    password: str = Body()


class TokenRetrieveSchemeOUT(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    key: str
    type: str = 'Bearer'
