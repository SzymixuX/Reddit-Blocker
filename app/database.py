import sqlite3

DB_NAME = "reddit_blocker.db"


def get_connection():
    return sqlite3.connect(DB_NAME)


def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS subreddits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            is_nsfw INTEGER DEFAULT 0,
            category TEXT,
            manual_blocked INTEGER DEFAULT 0,
            manual_allowed INTEGER DEFAULT 0,
            confidence REAL DEFAULT 1.0,
            source TEXT DEFAULT 'manual',
            description TEXT
        )
    """)

    conn.commit()
    conn.close()