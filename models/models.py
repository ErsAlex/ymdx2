import uuid
import enum
from sqlalchemy import types, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, declarative_base, relationship
from typing import List

from datetime import datetime

Base = declarative_base()


class User(Base):
    __tablename__ = "kv_users"

    id: Mapped[uuid.UUID] = mapped_column(types.UUID, primary_key=True, default=uuid.uuid4)
    user_name: Mapped[str] = mapped_column(nullable=False)
    user_surname: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.now, onupdate=datetime.now)
    created_projects: Mapped[List["Project"]] = relationship(back_populates="owner")
    created_tasks: Mapped[List["Task"]] = relationship(back_populates="owner")
    user_tariff: Mapped[List['UserTariff']] = relationship(back_populates="user")
    is_authenticated: Mapped[bool] = mapped_column(default=False)
    

class KeyType(str, enum.Enum):

    AUTH_KEY = "AUTH_KEY"

    PASS_RESET_KEY = "PASS_RESET_KEY"


class UserSecretKeys(Base):
    __tablename__ = 'kv_keys'
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[uuid.UUID] = mapped_column(types.UUID, nullable=True, default=None)
    email: Mapped[str] = mapped_column(nullable=True)
    key_type: Mapped[KeyType] = mapped_column(nullable=False)
    key: Mapped[str] = mapped_column(nullable=False)
    
class Tariff(Base):
    __tablename__ = "kv_tariffs"
    id: Mapped[int] = mapped_column(primary_key=True)
    tariff_name: Mapped[str] = mapped_column(nullable=False)
    price: Mapped[int] =  mapped_column(nullable=False)
    task_limit: Mapped[int] = mapped_column(nullable=False)
    day_limit: Mapped[int] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.now, onupdate=datetime.now)
    tariff_user: Mapped[List['UserTariff']] = relationship(back_populates="tariff")
    
class UserTariff(Base):
    __tablename__ = "kv_user_tariffs"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[uuid.UUID] = mapped_column(types.UUID, ForeignKey("kv_users.id"), unique=True)
    tariff_id: Mapped[int] = mapped_column(ForeignKey("kv_tariffs.id"))
    user: Mapped["User"] = relationship(back_populates="user_tariff")
    tariff: Mapped["Tariff"] = relationship(back_populates="tariff_user")
    
class Project(Base):
    __tablename__ = "kv_projects"
    id: Mapped[int] = mapped_column(primary_key=True)
    owner_id: Mapped[uuid.UUID] = mapped_column(types.UUID, ForeignKey("kv_users.id"))
    name: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.now, onupdate=datetime.now)
    owner: Mapped["User"] = relationship(back_populates="created_projects")
    tasks: Mapped[List["Task"]] = relationship(back_populates="project")
    

class TaskStatus(str, enum.Enum):

    WORKED = "WORKED"

    ERROR = "ERROR"


class Task(Base):
    __tablename__ = "kv_tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    owner_id: Mapped[uuid.UUID] = mapped_column(types.UUID, ForeignKey("kv_users.id"))
    project_id: Mapped[int] = mapped_column(ForeignKey("kv_projects.id"))
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.now, onupdate=datetime.now)
    url: Mapped[str] = mapped_column(nullable=True)
    message: Mapped[str] = mapped_column(nullable=True)
    status: Mapped[TaskStatus] = mapped_column(default=TaskStatus.WORKED)
    owner: Mapped["User"] = relationship(back_populates="created_tasks")
    project: Mapped["Project"] = relationship(back_populates="tasks")
