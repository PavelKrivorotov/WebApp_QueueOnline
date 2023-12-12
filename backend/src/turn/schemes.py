from datetime import datetime, timedelta
from typing import List

from pydantic import BaseModel, ConfigDict, field_serializer

from .models import QueueUser

# 
class QueueScheme(BaseModel):
    title: str
    queue_lifetime_key: str

class QueueCreateSchemeIN(QueueScheme):
    pass

class QueueRetrieveSchemeIN(BaseModel):
    key: str

class QueueDeleteSchemeIN(BaseModel):
    key: str

class QueueRetrieveSchemeOUT(QueueScheme):
    model_config = ConfigDict(from_attributes=True)
    
    key: str
    created: datetime
    is_active: bool

    @field_serializer('created')
    def serialize_created(value: datetime) -> str:
        return value.strftime('%d-%m-%Y %H:%M:%S')

class QueueListSchemeOUT(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    results: List[QueueRetrieveSchemeOUT]

# 
class QueueUserRetrieveSchemeOUT(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    position: int | None
    user_id: int
    queue_role: str

class QueueUserListSchemeOUT(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    results: List[QueueUserRetrieveSchemeOUT]


# 
class QueueLifetimeRetrieveSchemeOUT(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    key: str
    lifetime: timedelta

    @field_serializer('lifetime')
    def serialize_lifetime(value: timedelta) -> int:
        return value.seconds

class QueueLifetimeListSchemeOUT(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    results: List[QueueLifetimeRetrieveSchemeOUT]


# 
class ActionScheme(BaseModel):
    action_key: str

class ActionAddSchemeIN(ActionScheme):
    pass

class ActionAddExtendSchemeIN(ActionScheme):
    passive_queue_user_id: int

class ActionAddExtendSchemeOUT(ActionScheme):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    passive_queue_user: QueueUser

class ActionRetrieveSchemeOUT(ActionScheme):
    model_config = ConfigDict(from_attributes=True)
    
    active_user_id: int
    passive_user_id: int | None = None
    queue_key: str
    date: datetime

    @field_serializer('date')
    def serialize_date(value: datetime)  -> str:
        return value.strftime('%d-%m-%Y %H:%M:%S')


# 
class ActiveActionSchemeOUT(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    active_queue_user_id: int
    passive_queue_user_id: int
    action_key: str


# 
class ActionFullSchemeOUT(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    action: ActionRetrieveSchemeOUT

    user: QueueUserRetrieveSchemeOUT | None = None
    users: List[QueueUserRetrieveSchemeOUT] = []

    active_action: ActiveActionSchemeOUT | None = None
    active_actions: List[ActiveActionSchemeOUT] = []
