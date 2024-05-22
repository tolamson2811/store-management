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
    
class UserBase(BaseModel):
    email: str
    password: str
    
    class Config:
        orm_mode = True
        
class UserCreate(UserBase):
    username: str
    phone_number: str
    role: UserRole = UserRole.CUSTOMER
    wallet_balance: Decimal = 0.0
    created_at: datetime
        
    class Config:
        orm_mode = True
        
class UserUpdate(UserBase):
    email: Optional[str] = None
    password: Optional[str] = None
    username: Optional[str] = None
    phone_number: Optional[str] = None
    wallet_balance: Optional[Decimal] = None
    updated_at: datetime
        
    class Config:
        orm_mode = True
        
class UserLogin(UserBase):
    email: str
    password: str
        
    class Config:
        orm_mode = True

class UserChangePassword(UserBase):
    new_password: str
        
    class Config:
        orm_mode = True
        
class WalletCharge(BaseModel):
    amount: Decimal
        
    class Config:
        orm_mode = True

# transaction schemas
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