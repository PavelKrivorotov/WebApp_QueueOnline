from sqlalchemy.orm import Session

from .base import BaseAuthCRUD
from .models import User, Token
from .dependencies import BaseAuthDepends
from .schemes import UserCreateSchemeIN, TokenCreateSchemeIN
from .utils import make_hash_password, make_token


class AuthCRUD(BaseAuthCRUD):
    def __init__(self) -> None:
        pass

    def create(self, db: Session, data: UserCreateSchemeIN) -> User | None:
        user = self._retrieve_user(db, data.email)
        if (user is not None):
            return None

        user = User(
            email = data.email,
            first_name = data.first_name,
            last_name = data.last_name,
            password = make_hash_password(data.password)
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    def login(self, db: Session, data: TokenCreateSchemeIN) -> Token | None:
        user = self._retrieve_confirm_user(db, data.email, data.password)
        if (user is None):
            return None

        token = db.query(Token).where(Token.user_id == user.id).first()
        if (token is not None):
            refresh = self._refresh_token(db, token, user.id)
            return refresh
        
        token  = Token(
            key = make_token(),
            user_id = user.id
        )
        db.add(token)
        db.commit()
        db.refresh(token)
        return token

    def logout(self, db: Session, auth: BaseAuthDepends) -> None:
        db.delete(auth.token)
        auth.token = None
        db.commit()

    def _refresh_token(self, db: Session, token: Token, user_id: int) -> Token:
        # Magic refreshing...
        # 
        return token


auth = AuthCRUD()
