from logging import raiseExceptions
from jose import JWTError, jwt
from datetime import datetime,timedelta
from typing import Optional
from fastapi import FastAPI, Response, exceptions,status,HTTPException,Depends,APIRouter
from jose.constants import ALGORITHMS
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.sql.functions import user
from . import schemas,database,models
from sqlalchemy.orm import Session
from .config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY = settings.secret_key#"openssl rand -hex 32" to create a secret key in cmd
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_acces_token(token:str,credentials_exception):
    try:
        payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])

        user_id:str=payload.get("user_id")   
        if not user_id:
            raise  credentials_exception
        token_data=schemas.TokenData(user_id=user_id)  
    
    except JWTError as e:
        raise credentials_exception

    return token_data    

def get_current_user(token: str = Depends(oauth2_scheme),db:Session = Depends(database.get_db)) :
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"})

    token=verify_acces_token(token,credentials_exception)    
    user = db.query(models.User).filter(models.User.user_id==token.user_id).first()
    return  user     