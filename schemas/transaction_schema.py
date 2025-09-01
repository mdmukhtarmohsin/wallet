from typing import Optional
from pydantic import BaseModel, Field
import datetime
from enum import Enum

class TransactionType(str, Enum):
    CREDIT = "CREDIT"
    DEBIT = "DEBIT"
    TRANSFER_IN = "TRANSFER_IN"
    TRANSFER_OUT = "TRANSFER_OUT"

class Transaction(BaseModel):
    transaction_id:int
    transaction_type: TransactionType
    amount: float = Field(ge=0)
    description: str
    created_at: datetime.datetime

class TransactionsResponse(BaseModel):
    transactions: list[Transaction]
    total: int
    page: int
    limit: int

class TransactionDetailResponse(BaseModel):
    transaction_id:int
    user_id:int
    transaction_type:TransactionType
    amount: float = Field(ge=0)
    description: str
    recipient_user_id:Optional[int] = None
    reference_transaction_id:Optional[int] = None
    created_at: datetime.datetime   

