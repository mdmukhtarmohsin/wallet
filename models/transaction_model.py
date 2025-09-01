from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Enum, Numeric, ForeignKey
from typing import Optional
from db import Base
import datetime
import enum

# class TransactionType(str, Enum):
#     __tablename__ = "transaction_types"
#     CREDIT = "CREDIT"
#     DEBIT = "DEBIT"
#     TRANSFER_IN = "TRANSFER_IN"
#     TRANSFER_OUT = "TRANSFER_OUT"

class TransactionTypeEnum(enum.Enum):
    CREDIT = "CREDIT"
    DEBIT = "DEBIT"
    TRANSFER_IN = "TRANSFER_IN"
    TRANSFER_OUT = "TRANSFER_OUT"

class Transaction(Base):
    __tablename__ = "transactions"
    id: Mapped[int] = mapped_column( primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    transaction_type: Mapped[TransactionTypeEnum] = mapped_column()
    amount: Mapped[float] = mapped_column(Numeric(10, 2),default=0.00)
    description: Mapped[str] = mapped_column()
    reference_transaction_id: Mapped[Optional[int]] = mapped_column(ForeignKey("transactions.id"))
    recipient_user_id: Mapped[Optional[int]] = mapped_column(ForeignKey("users.id"))
    created_at: Mapped[datetime.datetime] = mapped_column( default=datetime.datetime.now)
