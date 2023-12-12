from typing import Any

from fastapi import WebSocket, WebSocketException, status
from sqlalchemy.orm import Session

from .dependencies import QueueAuthDepends
from .schemes import (
    ActionAddSchemeIN,
    ActionAddExtendSchemeIN,
    ActionAddExtendSchemeOUT,
    ActionFullSchemeOUT
)
from .services import turn


class WebSocketManager:
    _connections: dict[WebSocket, QueueAuthDepends] = {}

    def __init__(self) -> None:
        pass

    async def connect(self, websocket: WebSocket, auth: QueueAuthDepends) -> None:
        await websocket.accept()
        self._connections.setdefault(websocket, auth)

    def disconnect(self, websocket: WebSocket) -> None:
        self._connections.pop(websocket)

    async def manage(self, sender: WebSocket, auth: QueueAuthDepends, db: Session) -> None:
        data = await sender.receive_json()
        result = self._manage(data, auth, db)
        for key, value in self._connections.items():
            if value.queue.key == auth.queue.key:
                await key.send_json(result.model_dump())

    def _manage(self, raw_data: Any, auth: QueueAuthDepends, db: Session) -> ActionFullSchemeOUT:
        try:
            data = ActionAddSchemeIN.model_validate(raw_data)
            match data.action_key:
                # connect
                case 'QA00003':
                    action, queue_users, queue_user  = turn._action_connect(db, auth, data)
                    return ActionFullSchemeOUT.model_validate({
                        'action': action,
                        'users': queue_users,
                        'user': queue_user,
                    })

                # disconnect
                case 'QA00004':
                    return turn._action_disconnect(db, auth, data)

                # join
                case 'QA00005':
                    action, queue_users, queue_user = turn._action_join(db, auth, data)
                    return ActionFullSchemeOUT.model_validate({
                        'action': action,
                        'users': queue_users,
                        'user': queue_user,
                    })

                # leave
                case 'QA00006':
                    action, queue_users, queue_user = turn._action_leave(db, auth, data)
                    return ActionFullSchemeOUT.model_validate({
                        'action': action,
                        'users': queue_users,
                        'user': queue_user,
                    })

                # replace-offer
                case 'QA00007':
                    extend = self._extended_data(raw_data, auth, db)
                    action, queue_users, active_action = turn._action_replace_offer(db, auth, extend)
                    return ActionFullSchemeOUT.model_validate({
                        'action': action,
                        'users': queue_users,
                        'active_action': active_action
                    })

                # replace-accept
                case 'QA00008':
                    extend = self._extended_data(raw_data, auth, db)
                    action, queue_users, active_action = turn._action_replace_accept(db, auth, extend)
                    return ActionFullSchemeOUT.model_validate({
                        'action': action,
                        'users': queue_users,
                        'actions': active_action,
                    })

                # skip
                case 'QA00009':
                    extend = self._extended_data(raw_data, auth, db)
                    action, queue_users = turn._action_skip(db, auth, extend)
                    return ActionFullSchemeOUT.model_validate({
                        'action': action,
                        'users': queue_users,
                    })
        
        except Exception:
            raise WebSocketException(
                code = status.WS_1003_UNSUPPORTED_DATA,
                reason = 'Invalid input data! {}'.format(raw_data)
            )

    def _extended_data(
            self,
            raw_data: Any,
            auth: QueueAuthDepends,
            db: Session
        ) -> ActionAddExtendSchemeOUT:

        extend = ActionAddExtendSchemeIN.model_validate(raw_data)
        queue_user = turn._retrieve_queue_user_by_id(
            db,
            auth.queue.key,
            extend.passive_queue_user_id
        )
        # if queue_user is None... And rewrite _retrieve_queue_user_by_id function.

        return ActionAddExtendSchemeOUT(
            passive_queue_user = queue_user,
            action_key = extend.action_key
        )


websocket_manager = WebSocketManager()
