from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db import get_db
from schemas.transfer_schema import TransferRequest, TransferResponse, TransferErrorResponse, TransferDetailResponse
from models.transaction_model import Transaction as TransactionModel
from models.user_model import User as UserModel

router = APIRouter()

@router.post("/transfer")
def transfer(body: TransferRequest, db: Session = Depends(get_db)) -> TransferResponse:
    try:
        sender = db.query(UserModel).filter(UserModel.id == body.sender_user_id).first()
        recipient = db.query(UserModel).filter(UserModel.id == body.recipient_user_id).first()
        if not sender:
            raise HTTPException(status_code=404, detail="Sender not found")
        if not recipient:
            raise HTTPException(status_code=404, detail="Recipient not found")
        if float(sender.balance) < float(body.amount):
            raise HTTPException(status_code=400, detail="Insufficient balance")
        sender.balance = float(sender.balance) - float(body.amount)
        recipient.balance = float(recipient.balance) + float(body.amount)
        new_transaction_sender = TransactionModel(
            user_id=body.sender_user_id,
            transaction_type="TRANSFER_OUT",
            amount=body.amount,
            description=body.description,
            recipient_user_id=body.recipient_user_id
        )
        new_transaction_recipient = TransactionModel(
            user_id=body.recipient_user_id,
            transaction_type="TRANSFER_IN",
            amount=body.amount,
            description=body.description,
        )
        db.add(new_transaction_sender)
        db.add(new_transaction_recipient)
        db.commit()
        db.refresh(sender)
        db.refresh(recipient)
        db.refresh(new_transaction_sender)
        db.refresh(new_transaction_recipient)
        new_transaction_sender.reference_transaction_id = new_transaction_recipient.id
        new_transaction_recipient.reference_transaction_id = new_transaction_sender.id
        db.commit()
        return TransferResponse(
            sender_transaction_id=new_transaction_sender.id,
            recipient_transaction_id=new_transaction_recipient.id,
            amount=body.amount,
            sender_new_balance=sender.balance,
            recipient_new_balance=recipient.balance,
            status="SUCCESS"
        )
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))