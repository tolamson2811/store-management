from datetime import timedelta
from fastapi import security
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status
from database import get_db
from user import models
from user import schemas
from user import validation

from fastapi.security import HTTPAuthorizationCredentials, OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    if not await validation.validate_token(token):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return token

def get_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    response_data = []
    for user in users:
        response_data.append({
            "id": user.id,
            "email": user.email,
            "username": user.username,
            "phone_number": user.phone_number,
            "role": user.role,
            "wallet_balance": user.wallet_balance,
            "created_at": user.created_at,
            "updated_at": user.updated_at
        })
    return response_data

def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    if not validation.check_email_is_valid(user.email):
        raise HTTPException(status_code=400, detail="Invalid email")
    if not validation.check_email_is_unique(user.email, db):
        raise HTTPException(status_code=400, detail="Email already exists")
    if not validation.check_password_is_valid(user.password):
        raise HTTPException(status_code=400, detail="Invalid password")
    if not validation.check_username_is_valid(user.username):
        raise HTTPException(status_code=400, detail="Invalid username")
    if not validation.check_phone_number_is_valid(user.phone_number):
        raise HTTPException(status_code=400, detail="Invalid phone number")
    
    hashed_password = validation.get_password_hash(user.password)
    
    db_user = models.User(email=user.email, password=hashed_password, username=user.username, phone_number=user.phone_number, role=user.role, wallet_balance=user.wallet_balance, created_at=user.created_at)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    response_data = {
        "id": db_user.id,
        "email": db_user.email,
        "username": db_user.username,
        "phone_number": db_user.phone_number,
        "role": db_user.role,
        "wallet_balance": db_user.wallet_balance,
        "created_at": db_user.created_at
    }
    return response_data

def login_for_access_token(user: schemas.UserLogin, db: Session = Depends(get_db)):
    if not validation.check_email_is_valid(user.email):
        raise HTTPException(status_code=400, detail="Invalid email")
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="Email not exists")
    
    if not validation.verify_password(user.password, db_user.password):
        raise HTTPException(status_code=400, detail="Incorrect password")
    
    access_token_expires = timedelta(minutes=validation.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = validation.create_access_token(
        data={"sub": user.email, "role": db_user.role}, expires_delta=access_token_expires
    )
    return {
        "access_token": access_token,
        "expires_in": validation.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    }
    
def change_password(user: schemas.UserChangePassword, db: Session = Depends(get_db)):    
    if not validation.check_email_is_valid(user.email):
        raise HTTPException(status_code=400, detail="Invalid email")
    if not validation.check_password_is_valid(user.new_password):
        raise HTTPException(status_code=400, detail="Invalid password")
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    if not validation.verify_password(user.password, db_user.password):
        raise HTTPException(status_code=400, detail="Incorrect old password")
    
    hashed_password = validation.get_password_hash(user.new_password)

    db_user.password = hashed_password
    db.commit()
    db.refresh(db_user)
    
    return {
        "message": "Password changed successfully"
    }

def get_user_by_email(email: str, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == email).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    response_data = {
        "id": db_user.id,
        "email": db_user.email,
        "username": db_user.username,
        "phone_number": db_user.phone_number,
        "role": db_user.role,
        "wallet_balance": db_user.wallet_balance,
        "created_at": db_user.created_at
    }
    return response_data

def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    response_data = {
        "id": db_user.id,
        "email": db_user.email,
        "username": db_user.username,
        "phone_number": db_user.phone_number,
        "role": db_user.role,
        "wallet_balance": db_user.wallet_balance,
        "created_at": db_user.created_at
    }
    return response_data

def update_user(user_id: int, user: schemas.UserUpdate, db: Session = Depends(get_db), token: dict = None):  
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    if not validation.check_username_is_valid(user.username):
        raise HTTPException(status_code=400, detail="Invalid username")
    if not validation.check_phone_number_is_valid(user.phone_number):
        raise HTTPException(status_code=400, detail="Invalid phone number")
    if token['email'] != db_user.email and token['role'] != "admin":
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    if user.username is not None:
        db_user.username = user.username
    if user.phone_number is not None:
        db_user.phone_number = user.phone_number
    if user.wallet_balance is not None:
        db_user.wallet_balance = user.wallet_balance
    if user.email is not None:
        db_user.email = user.email
    if user.password is not None:
        db_user.password = validation.get_password_hash(user.password)
    
    db_user.updated_at = user.updated_at
    db.commit()
    db.refresh(db_user)
    
    response_data = {
        "id": db_user.id,
        "email": db_user.email,
        "username": db_user.username,
        "phone_number": db_user.phone_number,
        "role": db_user.role,
        "wallet_balance": db_user.wallet_balance,
        "created_at": db_user.created_at,
        "updated_at": db_user.updated_at
    }
    return response_data

def delete_user(user_id: int, db: Session = Depends(get_db), token: str = Depends(get_current_user)):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    if token['email'] != db_user.email and token['role'] != "admin":
        raise HTTPException(status_code=401, detail="Unauthorized")
    db.delete(db_user)
    db.commit()
    return {"message": "User deleted successfully"}

def create_transaction(transaction: schemas.TransactionCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.id == transaction.user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    db_transaction = models.Transaction(user_id=transaction.user_id)
    if transaction.transaction_type == "DEPOSIT":
        db_user.wallet_balance = db_user.wallet_balance + transaction.new_amount
    elif transaction.transaction_type == "WITHDRAW":
        if db_user.wallet_balance < transaction.new_amount:
            raise HTTPException(status_code=400, detail="Insufficient balance")
        db_user.wallet_balance = db_user.wallet_balance - transaction.new_amount 
    db_transaction.user_id = transaction.user_id
    db_transaction.old_amount = transaction.old_amount
    db_transaction.new_amount = transaction.new_amount
    db_transaction.transaction_type = transaction.transaction_type
    db_transaction.created_at = transaction.created_at
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    db.refresh(db_user)
    
    return db_transaction

def get_transactions(db: Session = Depends(get_db)):
    transactions = db.query(models.Transaction).all()
    return transactions

def get_transaction(transaction_id: int, db: Session = Depends(get_db)):
    db_transaction = db.query(models.Transaction).filter(models.Transaction.id == transaction_id).first()
    if db_transaction is None:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return db_transaction

def get_transaction_by_user_id(user_id: int, db: Session = Depends(get_db)):
    if not validation.check_user_id_valid(user_id, db):
        raise HTTPException(status_code=404, detail="User not found")
    
    db_transaction = db.query(models.Transaction).filter(models.Transaction.user_id == user_id).all()
    if db_transaction is None:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return db_transaction

def update_transaction(transaction_id: int, transaction: schemas.TransactionUpdateById, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.id == transaction.user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    db_transaction = db.query(models.Transaction).filter(models.Transaction.id == transaction_id).first()
    if not db_transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    
    if transaction.transaction_type == "DEPOSIT":
        db_user.wallet_balance = db_user.wallet_balance + transaction.new_amount
    elif transaction.transaction_type == "WITHDRAW":
        if db_user.wallet_balance < transaction.new_amount:
            raise HTTPException(status_code=400, detail="Insufficient balance")
        db_user.wallet_balance = db_user.wallet_balance - transaction.new_amount
        
    db_transaction.user_id = transaction.user_id
    db_transaction.old_amount = transaction.old_amount
    db_transaction.new_amount = transaction.new_amount
    db_transaction.transaction_type = transaction.transaction_type
    db_transaction.updated_at = transaction.updated_at
    db.commit()
    db.refresh(db_transaction, db_user)
    return db_transaction

def update_transaction_by_user_id(user_id: int, transaction: schemas.TransactionUpdateByUserId, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    db_transaction = db.query(models.Transaction).filter(models.Transaction.user_id == user_id).first()
    if not db_transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    
    if transaction.transaction_type == "DEPOSIT":
        db_user.wallet_balance = db_user.wallet_balance + transaction.new_amount
    elif transaction.transaction_type == "WITHDRAW":
        if db_user.wallet_balance < transaction.new_amount:
            raise HTTPException(status_code=400, detail="Insufficient balance")
        db_user.wallet_balance = db_user.wallet_balance - transaction.new_amount
        
    db_transaction.old_amount = transaction.old_amount
    db_transaction.new_amount = transaction.new_amount
    db_transaction.transaction_type = transaction.transaction_type
    db_transaction.updated_at = transaction.updated_at
    db.commit()
    db.refresh(db_transaction)
    return db_transaction

def delete_transaction(transaction_id: int, db: Session = Depends(get_db)):
    db_transaction = db.query(models.Transaction).filter(models.Transaction.id == transaction_id).first()
    if not db_transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    db.delete(db_transaction)
    db.commit()
    return {"message": "Transaction deleted successfully"}