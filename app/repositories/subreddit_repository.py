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

def get_all(category=None, is_nsfw=None, manual_blocked=None):
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

    return [row_to_subreddit_response(row) for row in rows]

def update(subreddit_name: str, update_data: dict):
    if not update_data:
        return False

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
    updated = cursor.rowcount > 0
    conn.close()

    return updated

def delete(subreddit_name: str):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM subreddits WHERE name = ?",
        (subreddit_name.lower(),)
    )

    conn.commit()
    deleted = cursor.rowcount > 0
    conn.close()

    return deleted

def get_stats():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM subreddits")
    total_subreddits = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM subreddits WHERE is_nsfw = 1")
    nsfw_subreddits = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM subreddits WHERE manual_blocked = 1")
    manual_blocked = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*)
        FROM subreddits
        WHERE is_nsfw = 0
        AND manual_blocked = 0
    """)
    allowed = cursor.fetchone()[0]

    conn.close()

    return {
        "total_subreddits": total_subreddits,
        "nsfw_subreddits": nsfw_subreddits,
        "manual_blocked": manual_blocked,
        "allowed": allowed
    }