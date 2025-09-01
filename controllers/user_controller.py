#file controller for user

from fastapi import APIRouter, Depends, HTTPException
from schemas.user_schema import UserCreateRequest, UserResponse, UserUpdateRequest
from models.user_model import User as UserModel
from db import get_db
from sqlalchemy.orm import Session

router = APIRouter()

@router.post("/users")
def create_user(user: UserCreateRequest, db: Session = Depends(get_db)) -> UserResponse:
    try:
        user = UserModel(
            username=user.username,
            email=user.email,
            password=user.password,
            phone_number=user.phone_number
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return UserResponse(
            id=user.id,
            username=user.username,
            email=user.email,
            phone_number=user.phone_number,
            balance=user.balance,
            created_at=user.created_at
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/users/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db)) -> UserResponse:
    try:
        user = db.query(UserModel).filter(UserModel.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return UserResponse(
            id=user.id,
            username=user.username,
            email=user.email,
            phone_number=user.phone_number,
            balance=user.balance,
            created_at=user.created_at
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/users/{user_id}")
def update_user(user_id: int, body: UserUpdateRequest, db: Session = Depends(get_db)) -> UserResponse:
    try:
        user = db.query(UserModel).filter(UserModel.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        user.username = body.username
        user.phone_number = body.phone_number
        db.commit()
        db.refresh(user)
        return UserResponse(
            id=user.id,
            username=user.username,
            email=user.email,
            phone_number=user.phone_number,
            balance=user.balance,
            created_at=user.created_at
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))