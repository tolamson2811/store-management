from database import get_db
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from product import models
from product import schemas
from product import validation


# Product controller 
def get_products(db: Session = Depends(get_db)):
    return db.query(models.Product).all()

def get_product_by_id(product_id: int, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    if not validation.check_product_group_valid(product.group_id, db):
        raise HTTPException(status_code=404, detail="Product group not found")
    if not validation.check_product_category_valid(product.category_id, db):
        raise HTTPException(status_code=404, detail="Product category not found")
    
    db_product = models.Product(name=product.name, image=product.image, price=product.price, discount_price=product.discount_price, quantity=product.quantity, description=product.description, supplier=product.supplier, group_id=product.group_id, category_id=product.category_id, created_at=product.created_at, updated_at=product.updated_at)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def update_product(product_id: int, product: schemas.ProductUpdate, db: Session = Depends(get_db)):
    db_product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    db_product.name = product.name
    db_product.price = product.price
    db_product.description = product.description
    db_product.updated_at = product.updated_at
    db.commit()
    db.refresh(db_product)
    return db_product

def delete_product(product_id: int, db: Session = Depends(get_db)):
    db_product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(db_product)
    db.commit()
    return {"message": "Product deleted successfully"}

# product group controller 
def get_product_groups(db: Session = Depends(get_db)):
    return db.query(models.ProductGroup).all()

def get_product_group_by_id(group_id: int, db: Session = Depends(get_db)):
    group = db.query(models.ProductGroup).filter(models.ProductGroup.id == group_id).first()
    if group is None:
        raise HTTPException(status_code=404, detail="Product group not found")
    return group

def create_product_group(group: schemas.ProductGroupCreate, db: Session = Depends(get_db)):
    db_group = models.ProductGroup(name=group.name, created_at=group.created_at)
    db.add(db_group)
    db.commit()
    db.refresh(db_group)
    return db_group

def update_product_group(group_id: int, group: schemas.ProductGroupUpdate, db: Session = Depends(get_db)):
    db_group = db.query(models.ProductGroup).filter(models.ProductGroup.id == group_id).first()
    if not db_group:
        raise HTTPException(status_code=404, detail="Product group not found")
    db_group.name = group.name
    db_group.updated_at = group.updated_at
    db.commit()
    db.refresh(db_group)
    return db_group

def delete_product_group(group_id: int, db: Session = Depends(get_db)):
    db_group = db.query(models.ProductGroup).filter(models.ProductGroup.id == group_id).first()
    if not db_group:
        raise HTTPException(status_code=404, detail="Product group not found")
    db.delete(db_group)
    db.commit()
    return {"message": "Product group deleted successfully"}

# product category controller 
def get_product_categories(db: Session = Depends(get_db)):
    return db.query(models.ProductCategory).all()

def get_product_category_by_id(category_id: int, db: Session = Depends(get_db)):
    category = db.query(models.ProductCategory).filter(models.ProductCategory.id == category_id).first()
    if category is None:
        raise HTTPException(status_code=404, detail="Product category not found")
    return category

def create_product_category(category: schemas.ProductCategoryCreate, db: Session = Depends(get_db)):
    if not validation.check_product_group_valid(category.group_id, db):
        raise HTTPException(status_code=404, detail="Product group not found")
    
    
    db_category = models.ProductCategory(name=category.name, group_id=category.group_id, created_at=category.created_at)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

def update_product_category(category_id: int, category: schemas.ProductCategoryUpdate, db: Session = Depends(get_db)):    
    db_category = db.query(models.ProductCategory).filter(models.ProductCategory.id == category_id).first()
    if not db_category:
        raise HTTPException(status_code=404, detail="Product category not found")
    db_category.name = category.name
    db_category.updated_at = category.updated_at
    db.commit()
    db.refresh(db_category)
    return db_category

def delete_product_category(category_id: int, db: Session = Depends(get_db)):
    db_category = db.query(models.ProductCategory).filter(models.ProductCategory.id == category_id).first()
    if not db_category:
        raise HTTPException(status_code=404, detail="Product category not found")
    db.delete(db_category)
    db.commit()
    return {"message": "Product category deleted successfully"}
