from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.schemas import Vote
from .database import engine
from .import models
from .routers import user,post,auth,vote
from .config import settings 



# models.Base.metadata.create_all(bind=engine) # this is the command to tell sqlalchemy to run create steatements 
#since we have alembic we dont need it 

app = FastAPI()

# origins=["https://www.google.com",
#          "https://www.youtube.com"
#          ]
origins=["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



    
 
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/")
def root():
    return {"message": "we will work a lot of things in 2022"}

#@app.get("/sqlalchemy")
#def test_posts(db: Session = Depends(get_db)):
    #return {"status":"success"}



