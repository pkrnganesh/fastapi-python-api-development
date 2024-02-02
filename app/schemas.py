from pydantic import BaseModel,EmailStr
from datetime import datetime
from typing import Optional
from pydantic.types import conint
class PostBase(BaseModel):
    title:str
    content:str
    published: bool = True

class PostCreate(PostBase):
    pass


class UserOut(BaseModel):
    id:int
    email: EmailStr
    created_at: datetime


    class Config:
        #  orm_mode = True   
          from_attributes = True
         
class Post(PostBase):
    id:int
    # title: str              
    # content: str                     since BaseModel is inherited so all these properties are already there
    # published: bool
    created_at: datetime
    owner_id: int
    owner: UserOut


    class Config:
        #  orm_mode = True     
         from_attributes = True  


class UserCreate(BaseModel):
    email: EmailStr       # a built one to evaluate the email from pydantic library
    password: str



class UserOut(BaseModel):
    id:int
    email: EmailStr
    created_at: datetime


    class Config:
     from_attributes = True      

class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id:Optional[str] = None


class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)  #lessthan or equalto