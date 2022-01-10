from fastapi import FastAPI, Response, exceptions,status,HTTPException,Depends,APIRouter
from ..import schemas,models,database, oauth2
from sqlalchemy.orm import Session
router=APIRouter(
    prefix="/vote",
    tags=["vote"]
)

@router.post("/",status_code=status.HTTP_201_CREATED)
def vote(vote:schemas.Vote,db: Session = Depends(database.get_db),current_user:int=Depends(oauth2.get_current_user)):
    
    vote_query=db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id==current_user.user_id)
    found_vote=vote_query.first()

    if vote.dir == 1: # to add an action of like
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
            detail=f'user id with {current_user.user_id} has already voted on {vote.post_id}')
        new_vote=models.Vote(post_id=vote.post_id,user_id=current_user.user_id) 
        db.add(new_vote)
        db.commit()
        return{"message":"succesfully voted"}
    elif vote.dir == 0: # to delete an action of like 
        if not found_vote:
           raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="vote does not exist for you ")

        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message":"succesfully deleted"}


