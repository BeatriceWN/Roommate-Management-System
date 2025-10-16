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

        def save(self):
        if self.id:
            return self.update()
        try:
            CURSOR.execute(
                "INSERT INTO roommates (name, room_number) VALUES (?, ?)",
                (self.name, self.room_number)
            )
            CONN.commit()
            self.id = CURSOR.lastrowid
            return self
        except sqlite3.IntegrityError as e:
            raise ValueError(f"Database error: {e}")

    def update(self):
        if not self.id:
            raise ValueError("Cannot update a roommate without an ID.")
        CURSOR.execute(
            "UPDATE roommates SET name=?, room_number=? WHERE id=?",
            (self.name, self.room_number, self.id)
        )
        CONN.commit()
        return self