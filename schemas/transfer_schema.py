from pydantic import BaseModel, Field
import datetime
from enum import Enum

class TransferRequest(BaseModel):
    sender_user_id:int
    recipient_user_id:int
    amount: float = Field(ge=0)
    description: str


class TransferResponse(BaseModel):
    sender_transaction_id: int
    recipient_transaction_id: int
    amount: float = Field(ge=0)
    sender_new_balance: float = Field(ge=0)
    recipient_new_balance: float = Field(ge=0)
    status: str

class TransferErrorResponse(BaseModel):
    error: str
    current_balance: float = Field(ge=0)
    required_amount: float = Field(ge=0)

class TransferDetailResponse(BaseModel):
    sender_user_id: int
    recipient_user_id: int
    amount: float = Field(ge=0)
    description: str
    status: str
    created_at: datetime.datetime
