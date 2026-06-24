from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
from database import create_tables, get_connection
from sqlite3 import IntegrityError

app = FastAPI()
create_tables()

class SubredditCreate(BaseModel):
    name: str
    is_nsfw: bool = False
    category: Optional[str] = None
    manual_blocked: bool = False
    manual_allowed: bool = False
    confidence: float = 1.0
    source: str = "manual"
    description: Optional[str] = None


class SubredditUpdate(BaseModel):
    is_nsfw: Optional[bool] = None
    category: Optional[str] = None
    manual_blocked: Optional[bool] = None
    manual_allowed: Optional[bool] = None
    confidence: Optional[float] = None
    source: Optional[str] = None
    description: Optional[str] = None

@app.get("/")
def home():
    return {"message": "Reddit Blocker API works"}

@app.get("/subreddits")
def get_subreddits():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT name, is_nsfw, category, manual_blocked, manual_allowed,
               confidence, source, description
        FROM subreddits
    """)

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

@app.get("/check/{subreddit_name}")
def check_subreddit(subreddit_name: str):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT name, is_nsfw, manual_blocked FROM subreddits WHERE LOWER(name) = LOWER(?)",
        (subreddit_name,)
    )

    row = cursor.fetchone()
    conn.close()

    if row is None:
        return {
            "subreddit": subreddit_name,
            "blocked": False,
            "reason": "not_found"
        }

    name = row[0]
    is_nsfw = bool(row[1])
    manual_blocked = bool(row[2])

    if is_nsfw:
        return {
            "subreddit": name,
            "blocked": True,
            "reason": "nsfw"
        }

    if manual_blocked:
        return {
            "subreddit": name,
            "blocked": True,
            "reason": "manual_blocked"
        }

    return {
        "subreddit": name,
        "blocked": False,
        "reason": "allowed"
    }

@app.post("/subreddits")
def add_subreddit(subreddit: SubredditCreate):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO subreddits (
                name, is_nsfw, category, manual_blocked, manual_allowed,
                confidence, source, description
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            subreddit.name.lower(),
            int(subreddit.is_nsfw),
            subreddit.category,
            int(subreddit.manual_blocked),
            int(subreddit.manual_allowed),
            subreddit.confidence,
            subreddit.source,
            subreddit.description
        ))

        conn.commit()

    except IntegrityError:
        conn.close()
        return {
            "message": "Subreddit already exists",
            "subreddit": subreddit.name.lower()
        }

    conn.close()

    return {
        "message": "Subreddit added",
        "data": subreddit
    }
@app.patch("/subreddits/{subreddit_name}")
def update_subreddit(subreddit_name: str, update: SubredditUpdate):
    update_data = update.model_dump(exclude_unset=True)

    if not update_data:
        return {"message": "No fields to update"}

    fields = []
    values = []

    for key, value in update_data.items():
        fields.append(f"{key} = ?")

        if isinstance(value, bool):
            values.append(int(value))
        else:
            values.append(value)

    values.append(subreddit_name.lower())

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        f"UPDATE subreddits SET {', '.join(fields)} WHERE name = ?",
        values
    )

    conn.commit()

    if cursor.rowcount == 0:
        conn.close()
        return {"message": "Subreddit not found"}

    conn.close()

    return {
        "message": "Subreddit updated",
        "updated_fields": update_data
    }
@app.delete("/subreddits/{subreddit_name}")
def delete_subreddit(subreddit_name: str):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM subreddits WHERE name = ?",
        (subreddit_name.lower(),)
    )

    conn.commit()

    if cursor.rowcount == 0:
        conn.close()
        return {"message": "Subreddit not found"}

    conn.close()

    return {
        "message": "Subreddit deleted",
        "subreddit": subreddit_name.lower()
    }