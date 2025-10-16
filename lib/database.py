import sqlite3

CONN = sqlite3.connect("db/database.db")
CONN.execute("PRAGMA foreign_keys = ON;")
CURSOR = CONN.cursor()

