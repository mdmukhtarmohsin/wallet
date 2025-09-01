from fastapi import APIRouter, Depends, HTTPException
from models.transaction_model import Transaction as TransactionModel
from schemas.transaction_schema import TransactionsResponse, TransactionDetailResponse,Transaction
from sqlalchemy.orm import Session
from db import get_db


router = APIRouter()

@router.get("/transactions/{user_id}")
def get_transactions(user_id: int,skip: int = 0, limit: int = 10 ,db: Session = Depends(get_db)) -> TransactionsResponse:
    try:
        transactions : list[TransactionModel] = db.query(TransactionModel).filter(TransactionModel.user_id == user_id).offset(skip).limit(limit).all()
        transctions_count = db.query(TransactionModel).filter(TransactionModel.user_id == user_id).count()
        return TransactionsResponse(
            transactions=[Transaction(
                transaction_id=transaction.id,
                transaction_type=transaction.transaction_type,
                amount=transaction.amount,
                description=transaction.description,
                created_at=transaction.created_at
            ) for transaction in transactions],
            total=transctions_count,
            page=skip,
            limit=limit
        )
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/transactions/detail/{transaction_id}")
def get_transaction(transaction_id: int, db: Session = Depends(get_db)) -> TransactionDetailResponse:
    try:
        transaction = db.query(TransactionModel).filter(TransactionModel.id == transaction_id).first()
        if not transaction:
            raise HTTPException(status_code=404, detail="Transaction not found")
        return TransactionDetailResponse(
            transaction_id=transaction.id,
            user_id=transaction.user_id,
            transaction_type=transaction.transaction_type,
            amount=transaction.amount,
            description=transaction.description,
            recipient_user_id=transaction.recipient_user_id if transaction.recipient_user_id else None,
            reference_transaction_id=transaction.reference_transaction_id if transaction.reference_transaction_id else None,
            created_at=transaction.created_at
        )
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))