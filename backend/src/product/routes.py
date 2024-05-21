from fastapi import APIRouter, Depends
from product import models
from product import controllers
from database import get_db
from sqlalchemy.orm import Session
from product import schemas

#product router
product_router = APIRouter(prefix="/product", tags=['Product'])

@product_router.get('/')
def get_products(db: Session = Depends(get_db)):
    return controllers.get_products(db)

@product_router.get('/{product_id}')
def get_product_by_id(product_id: int, db: Session = Depends(get_db)):
    return controllers.get_product_by_id(product_id, db)

@product_router.post('/', status_code=201)
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    return controllers.create_product(product, db)

@product_router.put('/{product_id}') 
def update_product(product_id: int, product: schemas.ProductUpdate, db: Session = Depends(get_db)):
    return controllers.update_product(product_id, product, db)

@product_router.delete('/{product_id}')
def delete_product(product_id: int, db: Session = Depends(get_db)):
    return controllers.delete_product(product_id, db)


# product group router
product_group_router = APIRouter(prefix="/product/group", tags=['Product Group'])

@product_group_router.get('/')
def get_product_groups(db: Session = Depends(get_db)):
    return controllers.get_product_groups(db)

@product_group_router.get('/{group_id}')
def get_product_group_by_id(group_id: int, db: Session = Depends(get_db)):
    return controllers.get_product_group_by_id(group_id, db)

@product_group_router.post('/', status_code=201)
def create_product_group(group: schemas.ProductGroupCreate, db: Session = Depends(get_db)):
    return controllers.create_product_group(group, db)

@product_group_router.put('/{group_id}')
def update_product_group(group_id: int, group: schemas.ProductGroupUpdate, db: Session = Depends(get_db)):
    return controllers.update_product_group(group_id, group, db)

@product_group_router.delete('/{group_id}')
def delete_product_group(group_id: int, db: Session = Depends(get_db)):
    return controllers.delete_product_group(group_id, db)


# product category router
product_category_router = APIRouter(prefix="/product/category", tags=['Product Category'])
@product_category_router.get('/')
def get_product_categories(db: Session = Depends(get_db)):
    return controllers.get_product_categories(db)

@product_category_router.get('/{category_id}')
def get_product_category_by_id(category_id: int, db: Session = Depends(get_db)):
    return controllers.get_product_category_by_id(category_id, db)

@product_category_router.post('/', status_code=201)
def create_product_category(category: schemas.ProductCategoryCreate, db: Session = Depends(get_db)):
    return controllers.create_product_category(category, db)

@product_category_router.put('/{category_id}')
def update_product_category(category_id: int, category: schemas.ProductCategoryUpdate, db: Session = Depends(get_db)):
    return controllers.update_product_category(category_id, category, db)

@product_category_router.delete('/{category_id}')
def delete_product_category(category_id: int, db: Session = Depends(get_db)):
    return controllers.delete_product_category(category_id, db)