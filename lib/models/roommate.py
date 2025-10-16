import sqlite3
from lib.database import CURSOR, CONN

class Roommate:
    def __init__(self, name, room_number, id=None):
        if not name or len(name.strip()) < 2:
            raise ValueError("Roommate name must be at least 2 characters long.")
        if not room_number:
            raise ValueError("Room number cannot be empty.")
        
        self.id = id
        self.name = name.strip()
        self.room_number = room_number.strip()