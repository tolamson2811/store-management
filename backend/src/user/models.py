from sqlalchemy import Column, Integer, String, TIMESTAMP, text, DECIMAL, ForeignKey
from sqlalchemy.orm import relationship

from database import Base

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    username = Column(String, index=True, nullable=False)
    phone_number = Column(String, index=True, nullable=False)
    role = Column(String, index=True, nullable=False)
    wallet_balance = Column(DECIMAL, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'))
    updated_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'))
    
    orders = relationship("Order", back_populates='user', cascade="all, delete")
    transactions = relationship("Transaction", back_populates='user', cascade="all, delete")
    
class Transaction(Base):
    __tablename__ = 'transactions'
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    old_amount = Column(DECIMAL, nullable=False)
    new_amount = Column(DECIMAL, nullable=False)
    total_amount = Column(DECIMAL)
    transaction_type = Column(String, nullable=False)
    
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'))
    updated_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'))
    
    user = relationship("User", back_populates='transactions')
    