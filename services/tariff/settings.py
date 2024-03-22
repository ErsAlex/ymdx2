from common.database.settings import BaseDatabaseSettings
from global_settings import DB_DSN
class TariffDatabaseSettings(BaseDatabaseSettings):
    db_dsn: str = DB_DSN