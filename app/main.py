from fastapi import FastAPI
from typing import Optional
from app.models import SubredditCreate, SubredditUpdate, SubredditResponse, StatsResponse
from app.database import create_tables, get_connection
from sqlite3 import IntegrityError
from fastapi.middleware.cors import CORSMiddleware
from app.routers.subreddits import router as subreddit_router
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

create_tables()
app.include_router(subreddit_router)