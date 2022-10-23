from sys import prefix
from fastapi import APIRouter, HTTPException, Response, status, Depends
import schemas, models, utils, oauth2
from database import *
from typing import Optional, List
from sqlalchemy.orm import Session

router = APIRouter(prefix="/user", tags=['users'])


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
def create_user(user: schemas.UserBase, db: Session = Depends(get_db)):
    # password hash
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get('/{id}', response_model=schemas.UserResponse)
async def get_user_byid(id:int, db: Session = Depends(get_db), current_user:int = Depends(oauth2.get_current_user)):
    user_data = db.query(models.User).filter(models.User.id == id).first()
    if user_data == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"id:{id} not found")
    return user_data