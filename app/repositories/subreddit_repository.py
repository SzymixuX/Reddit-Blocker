from sqlite3 import IntegrityError
from app.database import get_connection


def get_by_name(subreddit_name: str):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT name, is_nsfw, category, manual_blocked, manual_allowed,
               confidence, source, description
        FROM subreddits
        WHERE name = ?
    """, (subreddit_name.lower(),))

    row = cursor.fetchone()
    conn.close()

    return row

def row_to_subreddit_response(row):
    if row is None:
        return None

    return {
        "name": row[0],
        "is_nsfw": bool(row[1]),
        "category": row[2],
        "manual_blocked": bool(row[3]),
        "manual_allowed": bool(row[4]),
        "confidence": row[5],
        "source": row[6],
        "description": row[7]
    }

def create(subreddit):
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
        conn.close()
        return True

    except IntegrityError:
        conn.close()
        return False