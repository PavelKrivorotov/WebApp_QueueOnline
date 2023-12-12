from fastapi import WebSocketException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from .models import Queue, QueueUser, QueueAction


class BaseTurnCRUD:
    def __init__(self) -> None:
        pass
    
    @classmethod
    def _retrieve_queue(cls, db: Session, key: str) -> Queue | None:
        queue = db.query(Queue).where(Queue.key == key).first()
        return queue
    
    @classmethod
    def _retrieve_queue_action(cls, db: Session, key: str) -> QueueAction | None:
        queue_action = db.scalar(
            select(QueueAction)
            .where(
                QueueAction.key == key,
            )
        )
        return queue_action
    
    @classmethod
    def _retrieve_queue_user(cls, db: Session, key: str, user_id: int) -> QueueUser | None:
        queue_user = db.scalar(
            select(QueueUser)
            .where(
                QueueUser.queue_key == key,
                QueueUser.user_id == user_id,
            )
        )
        return queue_user
    
    @classmethod
    def _retrieve_queue_user_by_id(cls, db: Session, key: str, id: int) -> QueueUser:
        queue_user = db.scalar(
            select(QueueUser)
            .where(
                QueueUser.id == id,

                # Need for stop hack attack from another queue.
                QueueUser.queue_key == key
            )
        )

        if queue_user is None:
            raise WebSocketException(
                code = status.WS_1003_UNSUPPORTED_DATA,
                reason = 'Input error... Invalid passive_queue_user_id ({})'.format(
                    id
                )
            )
        return queue_user
