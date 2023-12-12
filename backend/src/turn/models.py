from typing import List

from sqlalchemy import Column, Integer, String, Boolean, Interval, Text, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.sql import func

from database import Base


class QueueLifetime(Base):
    __tablename__ = 'queue_lifetimes'

    key = Column(String(8), primary_key=True, index=True)
    lifetime = Column(Interval, unique=True)

    queues: Mapped[List["Queue"]] = relationship()


class Queue(Base):
    __tablename__ = 'queues'

    key = Column(String(64), primary_key=True, index=True)
    title = Column(String(150))
    created = Column(DateTime, server_default=func.now())
    is_active = Column(Boolean, default=True)

    user_id = Column(ForeignKey('users.id'))
    queue_lifetime_key = Column(ForeignKey('queue_lifetimes.key'))

    actions: Mapped[List["Action"]] = relationship()
    queue_users: Mapped[List["QueueUser"]] = relationship()


class QueueRole(Base):
    __tablename__ = 'queue_roles'

    key = Column(String(8), primary_key=True, index=True)
    role = Column(String(64), unique=True)
    detail = Column(Text)

    queue_users: Mapped[List["QueueUser"]] = relationship()


class QueueUser(Base):
    __tablename__ = 'queue_users'

    id = Column(Integer, primary_key=True, index=True)
    position = Column(Integer)

    user_id = Column(ForeignKey('users.id'))
    queue_key = Column(ForeignKey('queues.key'))
    queue_role = Column(ForeignKey('queue_roles.key'))

    active_actions_active_queue_users: Mapped[List["ActiveAction"]] = relationship(
        foreign_keys="ActiveAction.active_queue_user_id"
    )
    active_actions_passive_queue_users: Mapped[List["ActiveAction"]] = relationship(
        foreign_keys="ActiveAction.passive_queue_user_id"
    )


class QueueAction(Base):
    __tablename__ = 'queue_actions'

    key = Column(String(8), primary_key=True, index=True)
    action = Column(String(64), unique=True)
    detail = Column(Text)

    actions: Mapped[List["Action"]] = relationship()
    active_actions: Mapped[List["ActiveAction"]] = relationship()


class ActiveAction(Base):
    __tablename__ = 'active_actions'

    id = Column(Integer, primary_key=True, index=True)

    active_queue_user_id = Column(ForeignKey('queue_users.id'))
    passive_queue_user_id = Column(ForeignKey('queue_users.id'))
    action_key = Column(ForeignKey('queue_actions.key'))


class Action(Base):
    __tablename__ = 'actions'

    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime, server_default=func.now())
    active_user_position = Column(Integer)
    passive_user_position = Column(Integer) 

    active_user_id = Column(ForeignKey('users.id'))
    passive_user_id = Column(ForeignKey('users.id'))
    queue_key = Column(ForeignKey('queues.key'))
    action_key = Column(ForeignKey('queue_actions.key'))
