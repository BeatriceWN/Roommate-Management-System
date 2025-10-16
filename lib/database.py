import sqlite3

CONN = sqlite3.connect("db/database.db")
CONN.execute("PRAGMA foreign_keys = ON;")
CURSOR = CONN.cursor()

def create_tables():
    """Create tables for roommates, chores, bills, and roommate_bills"""

    CURSOR.execute("""
        CREATE TABLE IF NOT EXISTS roommates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            room_number TEXT
        )
    """)