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
            amount REAL NOT NULL,
            due_date TEXT,
            recurrence_type TEXT DEFAULT NULL,
            recurrence_day INTEGER DEFAULT NULL
        )
    """)

    CURSOR.execute("""
        CREATE TABLE IF NOT EXISTS roommate_bills (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            roommate_id INTEGER,
            bill_id INTEGER,
            share REAL,
            status TEXT DEFAULT 'pending',
            FOREIGN KEY (roommate_id) REFERENCES roommates(id) ON DELETE CASCADE,
            FOREIGN KEY (bill_id) REFERENCES bills(id) ON DELETE CASCADE
        )
    """)

    # Optional indexes
    CURSOR.execute("CREATE INDEX IF NOT EXISTS idx_chores_roommate_id ON chores(roommate_id);")
    CURSOR.execute("CREATE INDEX IF NOT EXISTS idx_roommate_bills_bill_id ON roommate_bills(bill_id);")
    CURSOR.execute("CREATE INDEX IF NOT EXISTS idx_roommate_bills_roommate_id ON roommate_bills(roommate_id);")

    CONN.commit()

if __name__ == "__main__":
    create_tables()
    CONN.close()
