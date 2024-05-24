from datetime import timedelta
from fastapi import security
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status
from database import get_db
from user import models
from user import schemas
from user import validation
from typing import List


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

def get_users(db: Session = Depends(get_db)) -> List[schemas.UserResponse]:
    users = db.query(models.User).all()
    
    if not users:
        raise HTTPException(status_code=404, detail="No users found")
    
    return [schemas.UserResponse.model_validate(user) for user in users]

def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)) -> schemas.UserResponse:
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
    
    return schemas.UserResponse.model_validate(db_user)

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

def get_user_by_email(email: str, db: Session = Depends(get_db)) -> schemas.UserResponse:
    db_user = db.query(models.User).filter(models.User.email == email).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    return schemas.UserResponse.model_validate(db_user)

def get_user_by_id(user_id: int, db: Session = Depends(get_db)) -> schemas.UserResponse:
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return schemas.UserResponse.model_validate(db_user)

def update_user(user_id: int, user: schemas.UserUpdate, db: Session = Depends(get_db), token: dict = None) -> schemas.UserResponse:  
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    update_data = user.model_dump(exclude_unset=True)
    
    if token['email'] != db_user.email and token['role'] != "admin":
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    if "password" in update_data:
        if not validation.check_password_is_valid(update_data['password']):
            raise HTTPException(status_code=400, detail="Invalid password")
        update_data['password'] = validation.get_password_hash(update_data['password'])
        
    if "username" in update_data:
        if not validation.check_username_is_valid(update_data['username']):
            raise HTTPException(status_code=400, detail="Invalid username")
        
    if "phone_number" in update_data:
        if not validation.check_phone_number_is_valid(update_data['phone_number']):
            raise HTTPException(status_code=400, detail="Invalid phone number")
    
    db.query(models.User).filter(models.User.id == user_id).update(update_data)
    db.commit()
    db.refresh(db_user)
    
    return schemas.UserResponse.model_validate(db_user)

def delete_user(user_id: int, db: Session = Depends(get_db), token: str = Depends(get_current_user)):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    if token['email'] != db_user.email and token['role'] != "admin":
        raise HTTPException(status_code=401, detail="Unauthorized")
    db.delete(db_user)
    db.commit()
    return {"message": "User deleted successfully"}


# transaction controller 
def create_transaction(transaction: schemas.TransactionCreate, db: Session = Depends(get_db)) -> schemas.TransactionResponse:
    db_user = db.query(models.User).filter(models.User.id == transaction.user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    if transaction.transaction_type == "DEPOSIT":
        db_user.wallet_balance += transaction.new_amount
    elif transaction.transaction_type == "WITHDRAW":
        if db_user.wallet_balance < transaction.new_amount:
            raise HTTPException(status_code=400, detail="Insufficient balance")
        db_user.wallet_balance -= transaction.new_amount 

    db_transaction = models.Transaction(**transaction.model_dump())
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    db.refresh(db_user)

    return schemas.TransactionResponse.model_validate(db_transaction)

def get_transactions(db: Session = Depends(get_db)) -> List[schemas.TransactionResponse]:
    transactions = db.query(models.Transaction).all()
    
    if not transactions:
        raise HTTPException(status_code=404, detail="No transactions found")
    
    return [schemas.TransactionResponse.model_validate(transaction) for transaction in transactions]

def get_transaction(transaction_id: int, db: Session = Depends(get_db)) -> schemas.TransactionResponse:
    db_transaction = db.query(models.Transaction).filter(models.Transaction.id == transaction_id).first()
    if db_transaction is None:
        raise HTTPException(status_code=404, detail="Transaction not found")
    
    return schemas.TransactionResponse.model_validate(db_transaction)

def get_transaction_by_user_id(user_id: int, db: Session = Depends(get_db)) -> List[schemas.TransactionResponse]:
    if not validation.check_user_id_valid(user_id, db):
        raise HTTPException(status_code=404, detail="User not found")
    
    db_transaction = db.query(models.Transaction).filter(models.Transaction.user_id == user_id).all()
    if db_transaction is None:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return [schemas.TransactionResponse.model_validate(transaction) for transaction in db_transaction]

def update_transaction(transaction_id: int, transaction: schemas.TransactionUpdateById, db: Session = Depends(get_db)) -> schemas.TransactionResponse:
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
        
    update_data = transaction.model_dump(exclude_unset=True)
    db.query(models.Transaction).filter(models.Transaction.id == transaction_id).update(update_data)
    
    db.commit()
    db.refresh(db_transaction)
    db.refresh(db_user)
    return schemas.TransactionResponse.model_validate(db_transaction)

def update_transaction_by_user_id(user_id: int, transaction: schemas.TransactionUpdateByUserId, db: Session = Depends(get_db)) -> schemas.TransactionResponse:
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
    
    db_transaction = db.query(models.Transaction).filter(models.Transaction.user_id == user_id).update(transaction.model_dump(exclude_unset=True))
    db.commit()
    db.refresh(db_transaction)
    return schemas.TransactionResponse.model_validate(db_transaction)

def delete_transaction(transaction_id: int, db: Session = Depends(get_db)):
    db_transaction = db.query(models.Transaction).filter(models.Transaction.id == transaction_id).first()
    if not db_transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    db.delete(db_transaction)
    db.commit()
    return {"message": "Transaction deleted successfully"}