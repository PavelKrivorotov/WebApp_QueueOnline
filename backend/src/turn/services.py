from typing import List

from sqlalchemy import select, update, func
from sqlalchemy.orm import Session

from auth.base import BaseAuthCRUD

from .base import BaseTurnCRUD
from .dependencies import QueueAuthDepends, is_member, is_not_member, is_lead
from .models import Queue, QueueUser, QueueLifetime, ActiveAction, Action
from .schemes import (
    QueueCreateSchemeIN,
    QueueRetrieveSchemeIN,
    QueueDeleteSchemeIN,
    ActionAddSchemeIN,
    ActionAddExtendSchemeOUT
)
from .utils import make_queue_key


class TurnCRUD(BaseAuthCRUD, BaseTurnCRUD):
    def __init__(self) -> None:
        pass

    def create(self, db: Session, data: QueueCreateSchemeIN, user_id: int) -> Queue:
        queue_key = make_queue_key()
        queue = Queue(
            key = queue_key,
            title = data.title,
            is_active = True,
            user_id = user_id,
            queue_lifetime_key = data.queue_lifetime_key,
        )

        queue_user = QueueUser(
            position = 1,
            queue_key = queue_key,
            user_id = user_id,
            queue_role = 'QR00003'
        )

        action = Action(
            active_user_position = 1,
            passive_user_position = None,
            active_user_id = user_id,
            passive_user_id = None,
            queue_key = queue_key,
            action_key = 'QA00001',
        )

        db.add_all([
            queue,
            queue_user,
            action,
        ])
        db.commit()
        db.refresh(queue)

        return queue
    
    def delete(self, db: Session, path: QueueDeleteSchemeIN, user_id: int) -> Queue | None:
        queue = self._retrieve_queue(db, path.key)
        if (queue is None):
            return None

        queue.is_active = False

        action = Action(
            active_user_position = 1,
            passive_user_position = None,
            active_user_id = user_id,
            passive_user_id = None,
            queue_key = queue.key,
            action_key = 'QA00002',
        )

        db.add(action)
        db.commit()
        db.refresh(queue)

        return queue
    
    def retrieve(self, db: Session, path: QueueRetrieveSchemeIN) -> Queue | None:
        return self._retrieve_queue(db, path.key)

    def action(
            self,
            db: Session,
            auth: QueueAuthDepends,
            data: ActionAddSchemeIN
        ) -> tuple[Action, List[QueueUser], QueueUser | None]:

        match data.action_key:
            # connect
            case 'QA00003':
                return self._action_connect(db, auth, data)

            # disconnect
            case 'QA00004':
                return self._action_disconnect(db, auth, data)

            # join
            case 'QA00005':
                return self._action_join(db, auth, data)

            # leave
            case 'QA00006':
                return self._action_leave(db, auth, data)

            # replace-offer
            case 'QA00007':
                return self._action_replace_offer(db, auth, data)

            # replace-accept
            case 'QA00008':
                return self._action_replace_accept(db, auth, data)

            # skip
            case 'QA00009':
                return self._action_skip(db, auth, data)

    def _action_connect(
            self,
            db: Session,
            auth: QueueAuthDepends,
            data: ActionAddSchemeIN
        ) -> tuple[Action, List[QueueUser], QueueUser]:

        action = self._make_raw_action(
            None,
            auth.user.id,
            auth.queue.key,
            data.action_key
        )
        db.add(action)
        db.commit()
        db.refresh(action)

        queue_users = self.list_queue_users(db, auth.queue.key)
        return (action, queue_users, auth.queue_user)

    def _action_disconnect(
            self,
            db: Session,
            auth: QueueAuthDepends,
            data: ActionAddSchemeIN
        ) -> Action:
        
        pass

    @is_not_member
    def _action_join(
            self,
            db: Session,
            auth: QueueAuthDepends,
            data: ActionAddSchemeIN
        # ) -> tuple[Action, List[QueueUser], QueueUser | None]:
        ) -> tuple[Action, List[QueueUser], QueueUser]:

        count = db.scalar(
            select(func.count(QueueUser.id))
            .where(
                QueueUser.queue_key == auth.queue.key,
                QueueUser.queue_role != 'QR00001'
            )
        )
        auth.queue_user.position = count + 1
        auth.queue_user.queue_role = 'QR00002'

        action = self._make_raw_action(
            count + 1,
            auth.user.id,
            auth.queue.key,
            data.action_key
        )

        db.add(action)
        db.commit()
        db.refresh(auth.queue_user)
        db.refresh(action)
        
        return (action, [auth.queue_user], auth.queue_user)

    @is_member
    def _action_leave(
            self,
            db: Session,
            auth: QueueAuthDepends,
            data: ActionAddSchemeIN
        # ) -> tuple[Action, List[QueueUser], QueueUser | None]:
        ) -> tuple[Action, List[QueueUser], QueueUser]:

        db.execute(
            update(QueueUser)
            .where(QueueUser.position > auth.queue_user.position)
            .values(position = QueueUser.position - 1)
        )

        action = self._make_raw_action(
            auth.queue_user.position,
            auth.user.id,
            auth.queue.key,
            data.action_key
        )

        # Check User is Lead or Member?
        # If Lead, then change is_staff in Queue.
        # 
        # Action `leader transfer` (The leader transfer to $1)??
        # 

        auth.queue_user.position = None
        auth.queue_user.queue_role = 'QR00001'

        db.add(action)
        db.commit()
        db.refresh(auth.queue_user)
        db.refresh(action)

        queue_users = self.list_queue_users(db, auth.queue.key)
        return (action, queue_users, auth.queue_user)

# 
# 
# 
# 
    def _action_replace_offer(
            self,
            db: Session,
            auth: QueueAuthDepends,
            # data: ActionAddSchemeIN
            data: ActionAddExtendSchemeOUT
        # ) -> tuple[Action, List[QueueUser], None, List[ActiveAction]]:
        # ) -> tuple[Action, List[QueueUser], List[ActiveAction]]:
        ) -> tuple[Action, List[QueueUser], ActiveAction]:

        # 
        # 
        # passive_queue_user = db.scalar(
        #     select(QueueUser)
        #     .where(
        #         QueueUser.id == data.passive_queue_user_id,

        #         # Need for stop hack attack from another queue.
        #         QueueUser.queue_key == auth.queue.key
        #     )
        # )
        # 
        # 

        # try:
        #     passive_queue_user = self._retrieve_queue_user_by_id(
        #         db,
        #         auth.queue.key,
        #         data.passive_queue_user_id
        #     )
        # except WebSocketException as e:
        #     raise e

        active_action = ActiveAction(
            active_queue_user_id = auth.queue_user.id,
            passive_queue_user_id = data.passive_queue_user.id,
            action_key = data.action_key
        )

        action = self._make_raw_action(
            auth.user.id,
            auth.user.id,
            auth.queue.key,
            data.action_key,
            data.passive_queue_user.position,
            data.passive_queue_user.user_id
        )

        db.add_all([
            active_action,
            action
        ])
        db.commit()
        db.refresh(active_action)
        db.refresh(action)

        return (action, [], None, [active_action])

    def _action_replace_accept(self,
            db: Session,
            auth: QueueAuthDepends,
            # data: ActionAddSchemeIN
            data: ActionAddExtendSchemeOUT
        # ) -> tuple[Action, List[QueueUser], None]:
        ) -> tuple[Action, List[QueueUser], List[ActiveAction]]:

        pass
# 
# 
# 
# 

    @is_member
    def _action_skip(
            self,
            db: Session,
            auth: QueueAuthDepends,
            data: ActionAddExtendSchemeOUT
        ) -> tuple[Action, List[QueueUser]]:

        tmp_position = auth.queue_user.position

        auth.queue_user.position = data.passive_queue_user.position
        data.passive_queue_user.position = tmp_position

        action = self._make_raw_action(
            auth.queue_user.position,
            auth.user.id,
            auth.queue.key,
            data.action_key,
            data.passive_queue_user.position,
            data.passive_queue_user.user_id
        )

        db.add(action)
        db.commit()
        db.refresh(auth.queue_user)
        db.refresh(data.passive_queue_user)
        db.refresh(action)

        queue_users = self.list_queue_users(db, auth.queue.key)
        return (action, queue_users)
        # return (action, [auth.queue_user, data.passive_queue_user])

    def _make_raw_action(
            self,
            active_user_position: int,
            active_user_id: int,
            queue_key: str,
            action_key: str,
            passive_user_position: int = None,
            passive_user_id: int = None
        ) -> Action:

        action = Action(
            active_user_position = active_user_position,
            passive_user_position = passive_user_position,
            active_user_id = active_user_id,
            passive_user_id = passive_user_id,
            queue_key  = queue_key,
            action_key = action_key
        )
        return action

    def list_queues(self, db: Session, user_id: int) -> List[Queue] | None:
        list = db.scalars(
            select(Queue)
            .join(Queue.queue_users)
            .where(
                QueueUser.user_id == user_id,
                QueueUser.queue_role != 'QR00001'
            )
            .order_by(Queue.created.desc())
        ).all()
        return list
    
    def list_actions(self, db: Session, queue_key: str) -> List[Action] | None:
        list = db.scalars(
            select(Action)
            .where(Action.queue_key == queue_key)
        ).all()
        return list

    def list_queue_users(self, db: Session, queue_key: str) -> List[QueueUser] | None:
        list = db.scalars(
            select(QueueUser)
            .where(
                QueueUser.queue_key == queue_key,
                QueueUser.queue_role != 'QR00001'
            )
            .order_by(QueueUser.position)
        ).all()
        return list

    def list_queue_lifetimes(self, db: Session) -> List[QueueLifetime] | None:
        list = db.scalars(
            select(QueueLifetime)
        ).all()
        return list


turn = TurnCRUD()
