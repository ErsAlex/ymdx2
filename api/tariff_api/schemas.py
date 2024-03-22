import uuid
from pydantic import BaseModel, ConfigDict, Field
from enum import Enum
import datetime



class TariffEnum(str, Enum):
    Demo = "Demo"
    Full = "Full"
    

class TariffSchema(BaseModel):
    
    model_config = ConfigDict(from_attributes=True)
    
    tariff_name: str
    price: int
    day_limit: int
    task_limit: int
    created_at: datetime.datetime
    updated_at: datetime.datetime
    

   
class AddTariffSchema(BaseModel):
    
    tariff: TariffEnum = Field(..., description="Выберите тариф", choices=[("Demo", "Demo"), ("Full", "Full")])


class UpdateTariffSchema(BaseModel):

    tariff: TariffEnum = Field(..., description="Выберите тариф", choices=[("Demo", "Demo"), ("Full", "Full")])