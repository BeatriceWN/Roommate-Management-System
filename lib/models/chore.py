import sqlite3
from lib.database import CURSOR, CONN

class Chore:
    def __init__(self, title, completed=False, roommate_id=None, id=None):
        if not title or len(title.strip()) < 2:
            raise ValueError("Chore title must be at least 2 characters long.")
        self.id = id
        self.title = title.strip()
        self.completed = bool(completed)
        self.roommate_id = roommate_id
