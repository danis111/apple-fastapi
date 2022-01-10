from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings
SQLALCHEMY_DATABASE_URL =f'postgresql://{settings.database_username}:{settings.database_password}@\
{settings.database_hostname}:{settings.database_port}/{settings.database_name}'
engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()












# import psycopg2
# from psycopg2.extras import RealDictCursor
# import time

# while True:
#     try:
#         conn=psycopg2.connect(host="localhost",database="fastapi",user="postgres",password="Melo.539933",
#         cursor_factory=RealDictCursor)
#         cursor=conn.cursor()
#         print("connection to db was achieved")
#         break
#     except Exception as error:
#         print("connection to db failed")
#         print("Error:", error)    
#         time.sleep(3)

# my_post=[]

#def find_post(id):
    #for p in my_post:
      # if  p["id"]== id:
          # return p

#def find_index_post(id):
    #for i,p in enumerate(my_post):
        #if p['id']==id:
            #return i 




