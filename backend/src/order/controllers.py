from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from order import models
from database import get_db
from order import validation

from order import schemas

def get_orders(db: Session = Depends(get_db)):
    return db.query(models.Order).all()

def get_order_by_id(order_id: int, db: Session = Depends(get_db)):
    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

def create_order(order: schemas.OrderUpdate, db: Session = Depends(get_db)):
    if not validation.check_user_id_valid(order.user_id, db):
        raise HTTPException(status_code=404, detail="User not found")
    
    db_order = models.Order(user_id=order.user_id, total_amount=order.total_amount, order_date = order.order_date)
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order

def update_order(order_id: int, order: schemas.OrderUpdate, db: Session = Depends(get_db)):
    if not validation.check_user_id_valid(order.user_id, db):
        raise HTTPException(status_code=404, detail="User not found")
    
    db_order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found")
    db_order.user_id = order.user_id
    db_order.total_amount = order.total_amount
    db_order.updated_at = order.updated_at
    db.commit()
    db.refresh(db_order)
    return db_order

def delete_order(order_id: int, db: Session = Depends(get_db)):
    db_order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found")
    db.delete(db_order)
    db.commit()
    return db_order

def get_order_by_id(order_id: int, db: Session = Depends(get_db)):
    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

def get_orders_by_user_id(user_id: int, db: Session = Depends(get_db)):
    orders = db.query(models.Order).filter(models.Order.user_id == user_id).all()
    if orders is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return orders

def get_orders_by_date(order_date: str, db: Session = Depends(get_db)):
    orders = db.query(models.Order).filter(models.Order.order_date >= order_date, models.Order.order_date <= order_date).all()
    if orders is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return orders

def get_orders_by_date_range(from_date: str, to_date: str, db: Session = Depends(get_db)):
    orders = db.query(models.Order).filter(models.Order.order_date >= from_date, models.Order.order_date <= to_date).all()
    if orders is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return orders

# order detail 
def get_all_order_details(db: Session = Depends(get_db)):
    return db.query(models.OrderDetail).all()

def get_order_details(order_id: int, db: Session = Depends(get_db)):
    order_details = db.query(models.OrderDetail).filter(models.OrderDetail.order_id == order_id).all()
    if order_details is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return order_details

def create_order_detail(order_detail: schemas.OrderDetailCreate, db: Session = Depends(get_db)):
    if not validation.check_order_id_valid(order_detail.order_id, db):
        raise HTTPException(status_code=404, detail="Order not found")
    
    db_order_detail = models.OrderDetail(order_id=order_detail.order_id, product_id=order_detail.product_id, quantity=order_detail.quantity, unit_price=order_detail.unit_price, created_at=order_detail.created_at)
    db.add(db_order_detail)
    db.commit()
    db.refresh(db_order_detail)
    return db_order_detail

def update_order_detail(order_detail_id: int, order_detail: schemas.OrderDetailUpdate, db: Session = Depends(get_db)):
    db_order_detail = db.query(models.OrderDetail).filter(models.OrderDetail.id == order_detail_id).first()
    if not db_order_detail:
        raise HTTPException(status_code=404, detail="Order Detail not found")
    db_order_detail.product_id = order_detail.product_id
    db_order_detail.quantity = order_detail.quantity
    db_order_detail.unit_price = order_detail.unit_price
    db_order_detail.updated_at = order_detail.updated_at
    db.commit()
    db.refresh(db_order_detail)
    return db_order_detail

def delete_order_detail(order_detail_id: int, db: Session = Depends(get_db)):
    db_order_detail = db.query(models.OrderDetail).filter(models.OrderDetail.id == order_detail_id).first()
    if not db_order_detail:
        raise HTTPException(status_code=404, detail="Order Detail not found")
    db.delete(db_order_detail)
    db.commit()
    return db_order_detail