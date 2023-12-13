from sqlalchemy.orm import Session

from .models import User, Token
from .utils import check_hash_password


class BaseAuthCRUD:
    def __init__(self) -> None:
        pass
    
    @classmethod
    def _retrieve_user(cls, db: Session, email: str) -> User | None:
        user = db.query(User).where(User.email == email).first()
        return user
    
    @classmethod
    def _retrieve_confirm_user(cls, db: Session, email: str, password: str) -> User | None:
        user = cls._retrieve_user(db, email)
        if (user is None):
            return None

        if (not check_hash_password(password, user.password)):
            return None
        
        return user
    
    @classmethod
    def _retrieve_token(cls, db: Session, token: str) -> Token | None:
        token = db.query(Token).where(Token.key == token).first()
        return token
