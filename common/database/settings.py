from pydantic_settings import BaseSettings
from pydantic import AnyUrl


class BaseDatabaseSettings(BaseSettings):
    db_dsn: AnyUrl