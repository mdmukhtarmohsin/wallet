from pydantic import BaseModel, Field
import datetime
from enum import Enum


class TransactionType(str, Enum):
    CREDIT = "CREDIT"
    DEBIT = "DEBIT"
    TRANSFER_IN = "TRANSFER_IN"
    TRANSFER_OUT = "TRANSFER_OUT"

class BalanceResponse(BaseModel):
    user_id: int
    balance: float = Field(ge=0)
    last_updated: datetime.datetime

class AddMoneyRequest(BaseModel):
    amount: float = Field(ge=0)
    description: str

class AddMoneyResponse(BaseModel):
    transaction_id: int
    user_id: int
    amount: float = Field(ge=0)
    new_balance: float = Field(ge=0)
    transaction_type: TransactionType

class WithdrawRequest(BaseModel):
    amount: float = Field(ge=0)
    description: str

class WithdrawResponse(BaseModel):
    transaction_id: int
    user_id: int
    amount: float = Field(ge=0)
    new_balance: float = Field(ge=0)
    transaction_type: TransactionType