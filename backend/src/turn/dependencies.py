import functools
from typing import Callable

from fastapi import HTTPException, WebSocketException, Depends, Query, Path, status
from sqlalchemy.orm import Session

from database import db_connection
from auth.dependencies import BaseAuthDepends

from .base import BaseTurnCRUD
from .models import Queue, QueueUser


class QueueAuthDepends(BaseAuthDepends):
    _db_field = 'is_active'

    queue: Queue = None
    queue_user: QueueUser = None

    def __init__(
            self,
            key: str = Path(),
            token: str = Query(),
            db: Session = Depends(db_connection)
        ) -> None:

        super().__init__(token, db)
        self.queue = self.verify_queue_key(key)

    def verify_queue_key(self, key: str) -> Queue:
        queue = BaseTurnCRUD._retrieve_queue(self._db, key)
        if queue is None:
            raise HTTPException(
                status_code = status.HTTP_400_BAD_REQUEST,
                detail = 'Queue key {} is invalid!'.format(key)
            )
        
            # raise WebSocketException(
            #     code = status.WS_1003_UNSUPPORTED_DATA,
            #     reason = 'Queue key {} is invalid!'.format(key)
            # )
        
        self.queue_user = BaseTurnCRUD._retrieve_queue_user(self._db, key, self.user.id)
        if self.queue_user is None:
            queue_user = QueueUser(
                position = None,
                queue_key = queue.key,
                user_id = self.user.id,
                queue_role = 'QR00001'
            )
            self._db.add(queue_user)
            self._db.commit();
            self._db.refresh(queue_user)

            self.queue_user = queue_user

        return queue

def is_member(function: Callable):
    @functools.wraps(function)
    def wraper(*args, **kwargs):
        auth: QueueAuthDepends = args[2]
        if not auth.queue_user:
            raise WebSocketException(
                code = status.WS_1008_POLICY_VIOLATION,
                reason = 'Only group members allowed!'
            )
        return function(*args, **kwargs)
    return wraper

def is_not_member(function: Callable):
    @functools.wraps(function)
    def wraper(*args, **kwargs):
        auth: QueueAuthDepends = args[2]
        if auth.queue_user and auth.queue_user.queue_role != 'QR00001':
            raise WebSocketException(
                code = status.WS_1008_POLICY_VIOLATION,
                reason = 'Only not members allowed!'
            )
        return function(*args, **kwargs)
    return wraper


def is_lead(function: Callable):
    @functools.wraps(function)
    def wraper(*args, **kwargs):
        auth: QueueAuthDepends = args[2]
        if auth.user.id != auth.queue.user_id:
            raise WebSocketException(
                code = status.WS_1008_POLICY_VIOLATION,
                reason = 'Only lead of group allowed!'
            )
        return function(*args, **kwargs)
    return wraper
