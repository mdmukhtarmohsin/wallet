#user model

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Numeric
from db import Base
import datetime


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column( primary_key=True, index=True)
    username: Mapped[str] = mapped_column( unique=True, index=True)
    email: Mapped[str] = mapped_column( unique=True, index=True)
    password: Mapped[str] = mapped_column()
    phone_number: Mapped[str] = mapped_column()
    balance: Mapped[float] = mapped_column(Numeric(10, 2), default=0.00)
    created_at: Mapped[datetime.datetime] = mapped_column( default=datetime.datetime.now)
    updated_at: Mapped[datetime.datetime] = mapped_column( default=datetime.datetime.now)