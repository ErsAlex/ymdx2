from pydantic import BaseModel, ConfigDict
import uuid
import datetime


class TaskCreateSchema(BaseModel):
    url: str
    message: str
    
class TaskUpdateSchema(BaseModel):
    url: str
    message: str
    
    
class TaskResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    owner_id: uuid.UUID
    url: str
    message: str
    created_at: datetime.datetime
    updated_at: datetime.datetime
    status: str
    
    