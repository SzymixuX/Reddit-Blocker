from fastapi import APIRouter
from sqlite3 import IntegrityError
from typing import Optional
from app.repositories import subreddit_repository
from app.database import get_connection
from app.models import (
    SubredditCreate,
    SubredditUpdate,
    SubredditResponse,
    StatsResponse
)
from app.services import blocking_service
router = APIRouter()

@router.get("/subreddits", response_model=list[SubredditResponse])
def get_subreddits(
    category: Optional[str] = None,
    is_nsfw: Optional[bool] = None,
    manual_blocked: Optional[bool] = None
):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
        SELECT name, is_nsfw, category, manual_blocked, manual_allowed,
               confidence, source, description
        FROM subreddits
    """

    conditions = []
    values = []

    if category is not None:
        conditions.append("category = ?")
        values.append(category)

    if is_nsfw is not None:
        conditions.append("is_nsfw = ?")
        values.append(int(is_nsfw))

    if manual_blocked is not None:
        conditions.append("manual_blocked = ?")
        values.append(int(manual_blocked))

    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    cursor.execute(query, values)

    rows = cursor.fetchall()
    conn.close()

    result = []

    for row in rows:
        result.append({
            "name": row[0],
            "is_nsfw": bool(row[1]),
            "category": row[2],
            "manual_blocked": bool(row[3]),
            "manual_allowed": bool(row[4]),
            "confidence": row[5],
            "source": row[6],
            "description": row[7]
        })

    return result

@router.get("/subreddits/{subreddit_name}", response_model=SubredditResponse)
def get_subreddits(
    category: Optional[str] = None,
    is_nsfw: Optional[bool] = None,
    manual_blocked: Optional[bool] = None
):
    return subreddit_repository.get_all(category, is_nsfw, manual_blocked)

@router.get("/check/{subreddit_name}")
def check_subreddit(subreddit_name: str):
    return blocking_service.check_subreddit(subreddit_name)

@router.post("/subreddits")
def add_subreddit(subreddit: SubredditCreate):
    created = subreddit_repository.create(subreddit)

    if not created:
        return {
            "message": "Subreddit already exists",
            "subreddit": subreddit.name.lower()
        }

    return {
        "message": "Subreddit added",
        "data": subreddit
    }
@router.patch("/subreddits/{subreddit_name}")
def update_subreddit(subreddit_name: str, update: SubredditUpdate):
    update_data = update.model_dump(exclude_unset=True)

    updated = subreddit_repository.update(subreddit_name, update_data)

    if not updated:
        return {"message": "Subreddit not found or no fields to update"}

    return {
        "message": "Subreddit updated",
        "updated_fields": update_data
    }
@router.delete("/subreddits/{subreddit_name}")
def delete_subreddit(subreddit_name: str):
    deleted = subreddit_repository.delete(subreddit_name)

    if not deleted:
        return {"message": "Subreddit not found"}

    return {
        "message": "Subreddit deleted",
        "subreddit": subreddit_name.lower()
    }

@router.get("/stats", response_model=StatsResponse)
def get_stats():
    return subreddit_repository.get_stats()