from typing import Annotated
from services.tariff.tariff_service import TariffDatabaseService, get_tariff_service
from fastapi import Depends
from services.user.auth_service import AuthService, get_auth_service
from common.auth.rest import get_user_id_from_token
import uuid
from models.models  import User

tariff_service = Annotated[TariffDatabaseService, Depends(get_tariff_service)]


