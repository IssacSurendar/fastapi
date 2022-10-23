from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr
from pydantic.types import conint

class PostBase(BaseModel):
    title: str
    content: str
    published: int = 0


class PostCreate(PostBase):
    pass

class UserResponse(BaseModel):
    id: int # required fields
    email: EmailStr
    created_at: datetime
    class Config:
        orm_mode = True

        
class Post(PostBase):
    id: int # required fields
    user_id: int
    created_at: datetime
    user :UserResponse

    class Config:
        orm_mode = True


class PostOut(BaseModel):
    Post: Post
    votes: int

    class Config:
        orm_mode = True
 

class UserBase(BaseModel):
    email: EmailStr
    password: str



        

class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None


class Vote(BaseModel):
    post_id : int
    dir : conint(le=1)