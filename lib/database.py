import sqlite3

CONN = sqlite3.connect("db/database.db")
CONN.execute("PRAGMA foreign_keys = ON;")
CURSOR = CONN.cursor()


def create_tables():
    """Create tables for roommates, chores, bills, and roommate_bills"""

    try:
        CURSOR.execute("""
            CREATE TABLE IF NOT EXISTS roommates (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                room_number TEXT UNIQUE NOT NULL
            )
        """)

        CURSOR.execute("""
            CREATE TABLE IF NOT EXISTS chores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                completed INTEGER DEFAULT 0,
                roommate_id INTEGER,
                FOREIGN KEY (roommate_id) REFERENCES roommates(id) ON DELETE SET NULL
            )
        """)

        CURSOR.execute("""
            CREATE TABLE IF NOT EXISTS bills (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                amount REAL NOT NULL CHECK (amount > 0),
                due_date TEXT,
                recurrence_type TEXT DEFAULT NULL,
                recurrence_day INTEGER DEFAULT NULL CHECK (recurrence_day BETWEEN 1 AND 31)
            )
        """)

        CURSOR.execute("""
            CREATE TABLE IF NOT EXISTS roommate_bills (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                roommate_id INTEGER NOT NULL,
                bill_id INTEGER NOT NULL,
                share REAL NOT NULL CHECK (share >= 0),
                status TEXT DEFAULT 'pending' CHECK (status IN ('pending', 'paid')),
                FOREIGN KEY (roommate_id) REFERENCES roommates(id) ON DELETE CASCADE,
                FOREIGN KEY (bill_id) REFERENCES bills(id) ON DELETE CASCADE,
                UNIQUE (roommate_id, bill_id)
            )
        """)

        CONN.commit()
        print("Database tables created or verified successfully.")

    except sqlite3.Error as e:
        print(f"Error creating tables: {e}")
        CONN.rollback()


def close_connection():
    """Safely close the database connection."""
    try:
        if CONN:
            CONN.close()
            print("Database connection closed.")
    except sqlite3.Error as e:
        print(f"Error closing connection: {e}")


if __name__ == "__main__":
    create_tables()
    close_connection()

