from typing import List

from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.sql import func

from database import Base
from turn.models import Queue, Action, QueueUser


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(150))
    last_name = Column(String(150))
    email = Column(String(150), unique=True, index=True)
    password = Column(String(128))

    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)

    tokens: Mapped[List["Token"]] = relationship()
    queues: Mapped[List["Queue"]] = relationship()

    action_active_users: Mapped[List["Action"]] = relationship(foreign_keys="Action.active_user_id")
    action_passive_users: Mapped[List["Action"]] = relationship(foreign_keys="Action.passive_user_id")
    queue_users: Mapped[List["QueueUser"]] = relationship()


class Token(Base):
    __tablename__  = 'tokens'
    
    key = Column(String(64), primary_key=True, index=True)
    date = Column(DateTime, server_default=func.now(), onupdate=func.now())

    user_id = Column(ForeignKey('users.id'), unique=True)
