import sqlite3

CONN = sqlite3.connect("db/database.db", detect_types=sqlite3.PARSE_DECLTYPES)
CONN.execute("PRAGMA foreign_keys = ON;")
CURSOR = CONN.cursor()

def get_connection():
    """Return a new database connection with foreign keys enabled."""
    conn = sqlite3.connect("db/database.db", detect_types=sqlite3.PARSE_DECLTYPES)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn