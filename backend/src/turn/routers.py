from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from database import db_connection
from auth.dependencies import IsAuthenticated

from .dependencies import QueueAuthDepends
from .schemes import (
    QueueCreateSchemeIN,
    QueueRetrieveSchemeIN,
    QueueDeleteSchemeIN,
    QueueRetrieveSchemeOUT,
    QueueListSchemeOUT,
    QueueUserRetrieveSchemeOUT,
    QueueUserListSchemeOUT,
    QueueLifetimeListSchemeOUT,
)
from .services import turn
from .managers import websocket_manager


router = APIRouter()

@router.post('/queue/create')
async def queue_create(
        data: QueueCreateSchemeIN,
        auth: IsAuthenticated = Depends(IsAuthenticated),
        db: Session = Depends(db_connection)
    ) -> JSONResponse:

    queue = turn.create(db, data, auth.user.id)
    return JSONResponse(
        content = QueueRetrieveSchemeOUT.model_validate(queue).model_dump(),
        status_code = status.HTTP_201_CREATED
    )

@router.get('/queue/retrieve/{key}')
async def queue_retrieve(
        path: QueueRetrieveSchemeIN = Depends(),
        auth: IsAuthenticated = Depends(IsAuthenticated),
        db: Session = Depends(db_connection)
    ) -> JSONResponse:
    
    queue = turn.retrieve(db, path)
    if queue is None:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = 'Queue key `{}` is invalid!'.format(path.key)
        )
    
    return JSONResponse(
        content = QueueRetrieveSchemeOUT.model_validate(queue).model_dump(),
        status_code = status.HTTP_200_OK
    )

@router.delete('/queue/delete/{key}')
async def queue_delete(
        # Neen = Depends()...
        path: QueueDeleteSchemeIN,
        auth: IsAuthenticated = Depends(IsAuthenticated),
        db: Session = Depends(db_connection)
    ) -> JSONResponse:

    obj = turn.delete(db, path, auth.user.id)
    if obj is None:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = "I dont know. May by queue with key={} is not exists".format(
                path.key,
            )
        )
    
    return JSONResponse(
        content = "Delete queue",
        status_code = status.HTTP_204_NO_CONTENT
    )

@router.get('/queue/queues')
async def queue_list(
        auth: IsAuthenticated = Depends(IsAuthenticated),
        db: Session = Depends(db_connection)
    ) -> JSONResponse:

    queues = turn.list_queues(db, auth.user.id)
    return JSONResponse(
        content = QueueListSchemeOUT.model_validate({
            'results': queues
        }).model_dump(),
        status_code = status.HTTP_200_OK
    )

@router.get('/queue/queue-users/{key}')
async def queue_users_list(
        path: QueueRetrieveSchemeIN = Depends(),
        auth: IsAuthenticated = Depends(IsAuthenticated),
        db: Session = Depends(db_connection)
    ) -> JSONResponse:

    users = turn.list_queue_users(db, path.key)
    return JSONResponse(
        content = QueueUserListSchemeOUT.model_validate({
            'results': users
        }).model_dump(),
        status_code = status.HTTP_200_OK
    )

@router.get('/queue/queue-lifetimes')
async def queue_lifetimes_list(
        db: Session = Depends(db_connection)
    ) -> JSONResponse:

    lifetimes = turn.list_queue_lifetimes(db)
    return JSONResponse(
        content = QueueLifetimeListSchemeOUT.model_validate({
            'results': lifetimes
        }).model_dump(),
        status_code = status.HTTP_200_OK
    )


@router.websocket('/queue/ws/{key}')
async def queue_ws(
        websocket: WebSocket,
        auth: QueueAuthDepends = Depends(QueueAuthDepends),
        db: Session = Depends(db_connection)
    ):

    await websocket_manager.connect(websocket, auth)
    try:
        while True:
            await websocket_manager.manage(websocket, auth, db)
    except WebSocketDisconnect:
        websocket_manager.disconnect(websocket)
