from fastapi import FastAPI, Response, exceptions,status,HTTPException,Depends,APIRouter
from starlette.status import HTTP_403_FORBIDDEN
from ..import models,schemas,oauth2
from typing import Optional,List
from sqlalchemy.orm import Session
from sqlalchemy import func
from ..database import engine,get_db


router=APIRouter(
    prefix="/posts",
    tags=["Posts"]
 
)

# @router.get("/",response_model=List[schemas.Post])
@router.get("/",response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db),current_user:int=Depends(oauth2.get_current_user),
limit:int =10,skip:int=0,search:Optional[str]=""):

    posts=db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()  #.filter(models.Post.owner_id==current_user.user_id) to just fetch posts that belong to user logged in
    
    results=db.query(models.Post,func.count(models.Post.id).label("votes")).join(
    models.Vote,models.Vote.post_id==models.Post.id,isouter=True).group_by(models.Post.id).filter(
    models.Post.title.contains(search)).limit(limit).offset(skip).all()
    #cursor.execute(""" SELECT *FROM posts """)
    #posts=cursor.fetchall()
    #print(posts)
    return results

@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.Post)
def create_post(post:schemas.PostCreate,db: Session = Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):

    #cursor.execute("""INSERT INTO posts (title,content,published) VALUES(%s,%s,%s)
    #RETURNING * """,(post.title,post.content,post.published))
    #new_post=cursor.fetchone()
    #conn.commit()
    #new_post=models.Post(title=post.title,content=post.content,published=post.published)

    new_post=models.Post(owner_id=current_user.user_id,**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.get("/{id}",response_model=schemas.PostOut)
def get_post(id : int,db: Session = Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):
    post=db.query(models.Post,func.count(models.Post.id).label("votes")).join(
    models.Vote,models.Vote.post_id==models.Post.id,isouter=True).group_by(models.Post.id).filter(models.Post.id==id).first()
    

    #cursor.execute(""" SELECT * FROM posts where id = %s  """,(str(id),))
    #post=cursor.fetchone()
    #conn.commit()
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id :{id} was not found")
    return post
#to delete a post from postgresql using fastAPI in python

@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int,db: Session = Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):
    post_query=db.query(models.Post).filter(models.Post.id==id)
    post=post_query.first()

    #cursor.execute("""DELETE FROM posts where id=%s RETURNING* """,(str(id),))
    #deleted_post=cursor.fetchone()
    #conn.commit()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post that you wanna delete doesnt exist")
    
    if post.owner_id != current_user.user_id:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN,detail='post that you wanna delete doesnt belong to you')
    post_query.delete(synchronize_session=False) 
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}",response_model=schemas.Post)
def update_post(id:int,updated_post:schemas.PostCreate,db: Session = Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):
    #cursor.execute("""UPDATE posts SET title=%s,content=%s,published=%s where id =%s RETURNING *""",
    #(post.title,post.content,post.published,str(id)))

    #conn.commit()
    #updated_post=cursor.fetchone()
    post_query=db.query(models.Post).filter(models.Post.id==id)
    post=post_query.first()
   
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post that you wanna update doesnt exist")
    

    if post.owner_id != current_user.user_id:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN,detail='post that you wanna update doesnt belong to you')   
    
    post_query.update(updated_post.dict(),synchronize_session=False)  
    db.commit()
    return post_query.first()