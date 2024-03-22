from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, create_async_engine
from contextlib import asynccontextmanager


class BaseDataBaseService:
    def __init__(self, dsn: str):
        self._dsn = dsn
        self._engine = create_async_engine(self._dsn, echo=False)
        self._sessionmaker = async_sessionmaker(self._engine, expire_on_commit=False)
        
    
        self.session = self._sessionmaker()
