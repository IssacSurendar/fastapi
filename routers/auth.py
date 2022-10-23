from sys import prefix
from fastapi import APIRouter, HTTPException, Response, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
import schemas, models, utils, oauth2
from database import *
from typing import Optional, List
from sqlalchemy.orm import Session

router = APIRouter(prefix="/auth", tags=['auth'])


@router.post('/login', response_model=schemas.Token)
async def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Email")

    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Credentials")

    access_token = oauth2.create_access_token(data ={"user_id": user.id})
    return {"token": access_token, "token_type": "bearer"}