from user import controllers
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from user import schemas

from database import get_db

from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from user import validation

security = HTTPBearer()

router = APIRouter(prefix="/user", tags=['User'])
transaction_router = APIRouter(prefix="/transaction", tags=['Transaction'])

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    data_authorize = await validation.validate_token(token)
    if not data_authorize:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return data_authorize

@router.get('')
def get_users(db: Session = Depends(get_db)):
    return controllers.get_users(db)

@router.get('/email/{email}')
def get_user_by_email(email: str, db: Session = Depends(get_db)):
    return controllers.get_user_by_email(email, db)

@router.get('/user_id/{user_id}')
def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    return controllers.get_user_by_id(user_id, db)
  
@router.post('', status_code=201)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return controllers.create_user(user, db)

@router.post('/login')
def login_user(user: schemas.UserLogin, db: Session = Depends(get_db)):
    return controllers.login_for_access_token(user, db)

@router.put('/{user_id}')
def update_user(user_id: int, user: schemas.UserUpdate, db: Session = Depends(get_db), token: dict = Depends(get_current_user)):
    return controllers.update_user(user_id, user, db, token)

@router.post('/change_password')
def change_password(user: schemas.UserChangePassword, db: Session = Depends(get_db), token: dict = Depends(get_current_user)):
    if token['email'] != user.email and token['role'] != 'admin':
        raise HTTPException(status_code=401, detail="Unauthorized")
    return controllers.change_password(user, db)

@router.delete('/{user_id}')
def delete_user(user_id: int, db: Session = Depends(get_db), token: dict = Depends(get_current_user)):
    return controllers.delete_user(user_id, db, token)

# transaction 
@transaction_router.get('')
def get_transactions(db: Session = Depends(get_db)):
    return controllers.get_transactions(db)

@transaction_router.get("/{transaction_id}")
def get_transaction(transaction_id: int, db: Session = Depends(get_db)):
    return controllers.get_transaction(transaction_id, db)

@transaction_router.get('/user/{user_id}')
def get_transactions(user_id: int, db: Session = Depends(get_db)):
    return controllers.get_transaction_by_user_id(user_id, db)

@transaction_router.post('', status_code=201)
def create_transaction(transaction: schemas.TransactionCreate, db: Session = Depends(get_db), token: dict = Depends(get_current_user)):
    return controllers.create_transaction(transaction, db)

@transaction_router.put('/{transaction_id}')
def update_transaction(transaction_id: int, transaction: schemas.TransactionUpdateById, db: Session = Depends(get_db), token: dict = Depends(get_current_user)):
    return controllers.update_transaction(transaction_id, transaction, db)

@transaction_router.put('/user/{user_id}')
def update_transaction_by_user_id(user_id: int, transaction: schemas.TransactionUpdateByUserId, db: Session = Depends(get_db), token: dict = Depends(get_current_user)):
    return controllers.update_transaction_by_user_id(user_id, transaction, db)

@transaction_router.delete('/{transaction_id}')
def delete_transaction(transaction_id: int, db: Session = Depends(get_db), token: dict = Depends(get_current_user)):
    return controllers.delete_transaction(transaction_id, db)
