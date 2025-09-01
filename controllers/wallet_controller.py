from fastapi import APIRouter, Depends, HTTPException
from schemas.wallet_schema import BalanceResponse, AddMoneyRequest, AddMoneyResponse, WithdrawRequest, WithdrawResponse
from models.user_model import User as UserModel
from models.transaction_model import Transaction as TransactionModel
from db import get_db
from sqlalchemy.orm import Session

router = APIRouter()

@router.get("/wallet/{user_id}/balance")
def get_wallet(user_id: int, db: Session = Depends(get_db)) -> BalanceResponse:
    try:
        user: UserModel = db.query(UserModel).filter(UserModel.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="Balance not found")
        return BalanceResponse(
            user_id=user_id,
            balance=user.balance,
            last_updated=user.created_at
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/wallet/{user_id}/add-money")
def add_money(user_id: int, body: AddMoneyRequest, db: Session = Depends(get_db)) -> AddMoneyResponse:
    try:
        user: UserModel = db.query(UserModel).filter(UserModel.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="Balance not found")
        user.balance = float(body.amount) + float(user.balance)
        new_transaction = TransactionModel(
            user_id=user_id,
            transaction_type="CREDIT",
            amount=body.amount,
            description=body.description,
        )
        db.add(new_transaction)
        db.commit()
        db.refresh(user)
        db.refresh(new_transaction)
        return AddMoneyResponse(
            transaction_id=new_transaction.id,
            user_id=user_id,
            amount=body.amount,
            new_balance=user.balance,
            transaction_type="CREDIT"
        )
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/wallet/{user_id}/withdraw")
def withdraw(user_id: int, body: WithdrawRequest, db: Session = Depends(get_db)) -> WithdrawResponse:
    try:
        user = db.query(UserModel).filter(UserModel.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        if float(user.balance) < float(body.amount):
            raise HTTPException(status_code=400, detail="Insufficient balance")
        user.balance = float(user.balance) - float(body.amount)
        new_transaction = TransactionModel(
            user_id=user_id,
            transaction_type="DEBIT",
            amount=body.amount,
            description=body.description,
        )
        db.add(new_transaction)
        db.commit()
        db.refresh(user)
        db.refresh(new_transaction)
        return WithdrawResponse(
            transaction_id=new_transaction.id,
            user_id=user_id,
            amount=body.amount,
            new_balance=user.balance,
            transaction_type="DEBIT"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))