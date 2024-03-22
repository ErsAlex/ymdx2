


from pydantic import BaseModel, ConfigDict
import uuid
import datetime

class ProjectCreateSchema(BaseModel):
    name: str
    description: str


class ProjectUpdateSchema(BaseModel):
    name: str
    description: str


class ProjectResponseSchema(BaseModel):

    model_config = ConfigDict(from_attributes=True)

    id: int
    owner_id: uuid.UUID
    created_at: datetime.datetime
    name: str
    description: str
