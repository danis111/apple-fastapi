from fastapi import FastAPI, Response, exceptions,status,HTTPException,Depends,APIRouter
from ..import models,schemas,utils
from typing import Optional,List
from sqlalchemy.orm import Session
from ..database import engine,get_db


router=APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.UserOut)
def create_user(user:schemas.UserCreate,db: Session = Depends(get_db)):
    hashed_password=utils.hash(user.password)
    user.password=hashed_password

    new_user=models.User(**user.dict())

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/{user_id}",response_model=schemas.UserOut)
def get_user(user_id : int,db: Session = Depends(get_db)):
    user=db.query(models.User).filter(models.User.user_id==user_id).first()
    

    #cursor.execute(""" SELECT * FROM posts where id = %s  """,(str(id),))
    #post=cursor.fetchone()
    #conn.commit()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"user {user_id} was not found")
    return user    