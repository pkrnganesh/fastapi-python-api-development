from typing import Optional,List
from fastapi import FastAPI,Response,status,HTTPException,Depends
from fastapi.responses import JSONResponse
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
from sqlalchemy.orm import Session
from . import models,schemas,utils
from .database import engine, get_db
from .routers import post,user,auth,vote
from .config import settings
from fastapi.middleware.cors import CORSMiddleware


# pwd_context = CryptContext(schemes=["bcrypt"],deprecated="auto")
# models.Base.metadata.create_all(bind=engine) this command in main.py file is used to or create statement  create tables using sqlalchemy now we have alembic so we are commenteing it

origins = ["*"]   #(cors policy)different types of origins or domains which can talk to us or allow us to fetch data or send request
#here above * denotes that every domain can access which means it is public api (or) ["http://www.google.com"] here only google server can access
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
    
app.include_router(post.router)  #including the router from post.py file
app.include_router(user.router)  #including the router from user.py file
app.include_router(auth.router)
app.include_router(vote.router)


@app.get("/", status_code=status.HTTP_201_CREATED)
def root():
    return {"message": "Hello World"}


# class Post(BaseModel):
#     title:str
#     content:str
#     published: bool = True   # from pydantic library  we imported a class called basemodel it checks the data sent by user is valid formate or not automatically



"""class update(BaseModel)
     title:str
     content:str
     published: bool = True    # insteaded of writing an another schema we could have used post schema above"""

  
"""my_posts = [{"title":"title of post 1","content":"content of post 1","id":1},{"title":"favourite foods","content":"i like pizza","id":2}]

def find_post(id):
    for p in my_posts:       #specific post in my_posts
        if p["id"] == id:      #here the id we pass must be equal to integer so in down we converted it into int(/posts/{id})
            return p
        

def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
           return i
        


@app.get("/")
def root():
    return {"message": "Hello World"}
  
@app.get("/sqlalchemy")
def test_posts(db:Session = Depends(get_db)):
    posts=db.query(models.Post).all()                  # posts=db.query(models.Post) here we have post model in models.py these actually returns a sql statement you can see it by printing posts  .all() helps to fetch  al the posts from database   
    
    return posts"""

    
