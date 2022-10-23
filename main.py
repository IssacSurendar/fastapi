from fastapi import FastAPI, HTTPException, Response, status, Depends
from database import *
from routers import posts, users, auth, vote


app = FastAPI()

app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(vote.router)


    
