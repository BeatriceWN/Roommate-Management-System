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

    def save(self):
        if self.id:
            return self.update()

        if self.roommate_id:
            roommate = CURSOR.execute("SELECT id FROM roommates WHERE id=?", (self.roommate_id,)).fetchone()
            if not roommate:
                raise ValueError(f"Roommate with ID {self.roommate_id} does not exist.")

        try:
            CURSOR.execute(
                "INSERT INTO chores (title, completed, roommate_id) VALUES (?, ?, ?)",
                (self.title, int(self.completed), self.roommate_id)
            )
            CONN.commit()
            self.id = CURSOR.lastrowid
            return self
        except sqlite3.IntegrityError as e:
            raise ValueError(f"Database error: {e}")

    def update(self):
        CURSOR.execute(
            "UPDATE chores SET title=?, completed=?, roommate_id=? WHERE id=?",
            (self.title, int(self.completed), self.roommate_id, self.id)
        )
        CONN.commit()
        return self

    @classmethod
    def all(cls):
        rows = CURSOR.execute("SELECT * FROM chores").fetchall()
        return [cls(id=row[0], title=row[1], completed=bool(row[2]), roommate_id=row[3]) for row in rows]

    @classmethod
    def find_by_roommate(cls, roommate_id):
        rows = CURSOR.execute("SELECT * FROM chores WHERE roommate_id=?", (roommate_id,)).fetchall()
        return [cls(id=row[0], title=row[1], completed=bool(row[2]), roommate_id=row[3]) for row in rows]

    def update_status(self, completed):
        if not isinstance(completed, bool):
            raise ValueError("Completed must be a boolean.")
        CURSOR.execute("UPDATE chores SET completed=? WHERE id=?", (int(completed), self.id))
        CONN.commit()
        self.completed = completed

    def delete(self):
        CURSOR.execute("DELETE FROM chores WHERE id=?", (self.id,))
        CONN.commit()

    def __repr__(self):
        status = "Complete" if self.completed else "Pending"
        return f"<Chore {self.id}: {self.title} | Status: {status} | Roommate ID: {self.roommate_id}>"