from pydantic import BaseModel
from typing import Optional
from enum import Enum
from datetime import datetime
from decimal import Decimal

class UserRole(str, Enum):
    ADMIN = "ADMIN"
    CUSTOMER = "CUSTOMER"
    EMPLOYEE = "EMPLOYEE"
    
class TransactionType(str, Enum):
    WITHDRAW = "WITHDRAW"
    DEPOSIT = "DEPOSIT"
    
class User(BaseModel):
    id: int
    email: str
    password: str
    username: str
    phone_number: str
    role: UserRole = UserRole.CUSTOMER
    wallet_balance: Decimal
    created_at: datetime
    updated_at: datetime
    
    class Config:
        orm_mode = True
        
class UserCreate(BaseModel):
    email: str
    password: str
    username: str
    phone_number: str
    role: UserRole = UserRole.CUSTOMER
    wallet_balance: Decimal = 0.0
    created_at: datetime
        
    class Config:
        orm_mode = True
        
class UserUpdate(BaseModel):
    username: Optional[str]
    phone_number: Optional[str]
    wallet_balance: Optional[Decimal]
    updated_at: datetime
        
    class Config:
        orm_mode = True
        
class UserLogin(BaseModel):
    email: str
    password: str
        
    class Config:
        orm_mode = True

class UserChangePassword(BaseModel):
    email: str
    old_password: str
    new_password: str
        
    class Config:
        orm_mode = True
        
class WalletCharge(BaseModel):
    amount: Decimal
        
    class Config:
        orm_mode = True
        
class Transaction(BaseModel):
    id: int
    user_id: int
    old_amount: Decimal
    new_amount: Decimal
    transaction_type: TransactionType
    created_at: datetime
    updated_at: datetime
    
    class Config:
        orm_mode = True
        
class TransactionCreate(BaseModel):
    user_id: int
    old_amount: Decimal
    new_amount: Decimal
    transaction_type: TransactionType
    created_at: datetime
        
    class Config:
        orm_mode = True
        
class TransactionUpdateById(BaseModel):
    user_id: int
    old_amount: Optional[Decimal]
    new_amount: Optional[Decimal]
    transaction_type: Optional[TransactionType]
    updated_at: datetime
        
    class Config:
        orm_mode = True

class TransactionUpdateByUserId(BaseModel):
    old_amount: Optional[Decimal]
    new_amount: Optional[Decimal]
    transaction_type: Optional[TransactionType]
    updated_at: datetime
        
    class Config:
        orm_mode = True