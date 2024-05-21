from pydantic import BaseModel
from datetime import datetime
from decimal import Decimal
from typing import Optional

# Order schema 
class Order(BaseModel):
    id: int
    user_id: int
    total_amount: Decimal
    order_date: datetime
    updated_at: datetime
    
    class Config:
        orm_mode = True
        
class OrderCreate(BaseModel):
    user_id: int
    total_amount: Decimal
    order_date: datetime
    
    class Config:
        orm_mode = True
        
class OrderUpdate(BaseModel):
    user_id: Optional[int]
    total_amount: Optional[Decimal]
    updated_at: datetime
    
    class Config:
        orm_mode = True
        
# Order detail schema 
class OrderDetail(BaseModel):
    id: int
    order_id: int
    product_id: int
    quantity: int
    unit_price: Decimal
    
    class Config:
        orm_mode = True
        
class OrderDetailCreate(BaseModel):
    order_id: int
    product_id: int
    quantity: int
    unit_price: Decimal
    created_at: datetime
    
    class Config:
        orm_mode = True
        
class OrderDetailUpdate(BaseModel):
    product_id: Optional[int]
    quantity: Optional[int]
    unit_price: Optional[Decimal]
    updated_at: datetime
    
    class Config:
        orm_mode = True