from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# Product schema
class Product(BaseModel):
    id: int
    name: str
    image: str
    price: float
    discount_price: float
    quantity: int
    description: str
    supplier: str
    group_id: int
    category_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        orm_mode = True
        
class ProductCreate(BaseModel):
    name: str
    image: str
    price: float
    discount_price: float
    quantity: int
    description: str
    supplier: str
    group_id: int
    category_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        orm_mode = True
        
class ProductUpdate(BaseModel):
    name: Optional[str]
    image: Optional[str]    
    price: Optional[float]
    discount_price: Optional[float]
    quantity: Optional[int]
    description: Optional[str]
    supplier: Optional[str]
    updated_at: datetime
    
    class Config:
        orm_mode = True
        
        
# Product group schema
class ProductGroup(BaseModel):
    id: int
    name: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        orm_mode = True
        
class ProductGroupCreate(BaseModel):
    name: str
    created_at: datetime
    
    class Config:
        orm_mode = True
        
class ProductGroupUpdate(BaseModel):
    name: Optional[str]
    updated_at: datetime
    
    class Config:
        orm_mode = True

# Product category schema
class ProductCategory(BaseModel):
    id: int
    name: str
    group_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        orm_mode = True
        
class ProductCategoryCreate(BaseModel):
    name: str
    group_id: int
    created_at: datetime
    
    class Config:
        orm_mode = True
    
class ProductCategoryUpdate(BaseModel):
    name: Optional[str]
    updated_at: datetime
    
    class Config:
        orm_mode = True

class ProductSearch(BaseModel):
    group_name: Optional[str] = None
    category_name: Optional[str] = None
    product_name: Optional[str] = None
    supplier: Optional[str] = None
    min_price: Optional[float] = None
    max_price: Optional[float] = None
    discount_price: Optional[bool] = None
    quantity: Optional[bool] = None
    
    class Config:
        orm_mode = True