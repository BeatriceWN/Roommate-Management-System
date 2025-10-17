import sqlite3

# Establish a connection to the database and enable foreign keys
CONN = sqlite3.connect("db/database.db")
CONN.execute("PRAGMA foreign_keys = ON;")
CURSOR = CONN.cursor()


def create_tables():
    """Create all required tables for the Roommate Management System."""

    try:
        # Table: roommates
        CURSOR.execute("""
            CREATE TABLE IF NOT EXISTS roommates (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                room_number TEXT UNIQUE NOT NULL
            )
        """)

        # Table: chores
        CURSOR.execute("""
            CREATE TABLE IF NOT EXISTS chores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                completed INTEGER DEFAULT 0,
                roommate_id INTEGER,
                FOREIGN KEY (roommate_id) REFERENCES roommates(id) ON DELETE SET NULL
            )
        """)

        # Table: bills
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

        # Table: roommate_bills (join table for roommates and bills)
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

        # Commit all changes to the database
        CONN.commit()

    except sqlite3.Error as e:
        print(f"Error creating tables: {e}")
        CONN.rollback()


def close_connection():
    """Close the database connection safely."""
    try:
        CONN.close()
    except sqlite3.Error as e:
        print(f"Error closing connection: {e}")
