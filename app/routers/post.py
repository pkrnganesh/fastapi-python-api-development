from .. import models,schemas,oauth2
from fastapi import FastAPI,Response,status,HTTPException,Depends,APIRouter
from sqlalchemy.orm import Session
from .. database import engine, get_db
from typing import Optional,List
from sqlalchemy import func

router = APIRouter(
    tags=['Posts']
)


@router.get("/posts",response_model=List[schemas.Post]) #since function returns multiple posts so we need to send a list of posts to response model to evaluate
def get_posts(db:Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user),
              limit: int = 10,skip: int = 0,search: Optional[str] = ""):# default limit set to 10 posts if we wont specify limit
    # cursor.execute("""SELECT * FROM posts""")
    # posts =  cursor.fetchall()
    # print(posts)
    # posts=db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all           # filter(models.Post.owner_id == current_user.id).all() getting only the posts of specified owner who is the user who currently loggedin
    # return posts #json converts this a variable similar to an array
     posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
     return posts

@router.post("/posts",status_code=status.HTTP_201_CREATED,response_model =schemas.Post)
def create_posts(post: schemas.PostCreate,db:Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)): #depends on oauth2 since we are forcing our application user to login to create a post
    #   cursor.execute("""INSERT INTO posts (title,content,published) VALUES (%s, %s, %s) RETURNING * """,
    #                  (post.title, post.content, post.published))
    #   new_post = cursor.fetchone()                   storing the values of post entered in frontend to varibales %s resp
      
    #   conn.commit()                                   making permanent changes in db  
      print(current_user.id)
      new_post = models.Post(owner_id = current_user.id,**post.model_dump())             #(title = post.title,content = post.content,published = post.published) instead of this we can actually unpack the model by **
      db.add(new_post)
      db.commit()
      db.refresh(new_post)
      return new_post                         # post_dict = post.model_dump()
                    
    #                                                   post_dict['id'] = randrange(0,100000)#since every entry must have an id this is done db at intially we are not actually working with it so we doing it in software
    #                                                   my_posts.append(post_dict)
    #                                                   return {"data": post_dict}


@router.get("/posts/{id}",response_model=schemas.Post)    #to retrive data of specific post here id will be string
def get_post(id:int,db:Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):    #changing id into integer (2.here it shows us it is path parameter error if we pass an string value instead of integer in path
    # cursor.execute("""select * from posts where id = %s""",str(id))                                         # print(id)
    # post = cursor.fetchone()  
    # post = db.query(models.Post).filter(models.Post.id == id).first()
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
    print(post)                             # post = find_post(id)    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail = f"post with id {id} was not found")
                                                    # post = find_post(int(id))1.here in this case it doesnt show actual error to the user it shows internal server error
    return post


# @app.delete("/posts/{id}")
# def delete_post(id: int,db:Session = Depends(get_db)):
#     # Find the index in the array that has the required id
#     # cursor.execute(""" DELETE FROM posts WHERE  id = %s returning *""",str(id))
#     # deleted_post =  cursor.fetchone()
#     #conn.commit()
#     post = db.query(models.Post).filter(models.Post.id == id)                          
#     if post.first() == None:            # here if the id gives none  it means find_post(id) is returning no data       
#         return {'message': 'Post was successfully deleted'}
#     # else:
#     #     # Return a 404 Not Found response if the post with the given id is not found
#     #     raise HTTPException(status_code=404, detail="Post not found")
   
#     else:
#         post.delete(synchronize_session=False)
#         db.commit()
#         raise HTTPException(status_code=404, detail="Post not found")
@router.delete("/posts/{id}")
def delete_post(id: int, db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=404, detail="Post not found")
    

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="NOT authorized to performe requiredaction")
    
    post_query.delete(synchronize_session=False)
    db.delete(post)
    db.commit()
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/posts/{id}",response_model=schemas.Post)
def update_post(id: int,updated_post:schemas.PostCreate,db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):  #changing id of string to int by using id: int
    # cursor.execute("""UPDATE posts SET title = %s, content = %s,published = %s WHERE id = %s RETURNING * """,(post.title,post.content,post.published),str(id))
    # updated_post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id==id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail = f"post with id: {id} does not exist")
    post_query.update(updated_post.model_dump(),synchronize_session=False)
    db.commit()
    return post_query.first()

