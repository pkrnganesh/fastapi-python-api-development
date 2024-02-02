from .. import models,schemas,utils
from fastapi import FastAPI,Response,status,HTTPException,Depends,APIRouter
from sqlalchemy.orm import Session
from .. database import engine, get_db

router = APIRouter(
     tags=['Users']        #in order to separate the user path operations in gui or fastapidocs
)

@router.post("/users",status_code=status.HTTP_201_CREATED,response_model=schemas.UserOut)
def create_user(user:schemas.UserCreate,db:Session = Depends(get_db)):

    #hash the password - user.password
    hashed_password = utils.hash(user.password)  #here we calling a hash named function in utils and that function retrns hashed password now we store it in db user.password
    user.password = hashed_password
    new_user = models.User(**user.model_dump())   # here what is actually happening is schemas nunchi vachinna user details ni dictionary loki marchi unpack chesthunam 
    db.add(new_user)                              #adding the user to the database
    db.commit()                                   #commiting the changes in db
    db.refresh(new_user)                          #refreshing to see the new user details

    return new_user

@router.get('/users/{id}',response_model=schemas.UserOut)
def get_user(id:int,db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"User with id: {id}")

    return user