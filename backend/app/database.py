import sqlite3
import os

DB_NAME = "clinic.db"


def get_connection():
    """
    Returns a SQLite connection.
    """
    return sqlite3.connect(DB_NAME)


def init_db():
    """
    Initialize database and ensure schema is up to date.
    Safe to run multiple times.
    """
    conn = get_connection()
    c = conn.cursor()

    # Create table if not exists (fresh install)
    c.execute("""
    CREATE TABLE IF NOT EXISTS bookings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        event_type_id INTEGER NOT NULL,
        start TEXT NOT NULL,
        end TEXT NOT NULL,
        name TEXT NOT NULL,
        email TEXT NOT NULL,
        meet_link TEXT
    );
    """)

    # --- Migration guard (for existing DBs) ---
    c.execute("PRAGMA table_info(bookings);")
    columns = [row[1] for row in c.fetchall()]

    if "meet_link" not in columns:
        c.execute("ALTER TABLE bookings ADD COLUMN meet_link TEXT;")

    conn.commit()
    conn.close()


# Initialize on import
init_db()
