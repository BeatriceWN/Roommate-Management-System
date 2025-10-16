import sqlite3
from lib.database import CURSOR, CONN


class Roommate:
    """Represents a roommate in the shared living system."""

    def __init__(self, name: str, room_number: str, id: int = None):
        if not name or len(name.strip()) < 2:
            raise ValueError("Roommate name must be at least 2 characters long.")
        if not room_number:
            raise ValueError("Room number cannot be empty.")

        self.id = id
        self.name = name.strip()
        self.room_number = room_number.strip()

    def save(self):
        """Save roommate to database or update if exists."""
        if self.id:
            return self.update()

        try:
            CURSOR.execute(
                "INSERT INTO roommates (name, room_number) VALUES (?, ?)",
                (self.name, self.room_number),
            )
            CONN.commit()
            self.id = CURSOR.lastrowid
            return self
        except sqlite3.IntegrityError as e:
            raise ValueError(f"Database error: {e}")

    def update(self):
        """Update roommate info."""
        if not self.id:
            raise ValueError("Cannot update a roommate without an ID.")
        CURSOR.execute(
            "UPDATE roommates SET name=?, room_number=? WHERE id=?",
            (self.name, self.room_number, self.id),
        )
        CONN.commit()
        return self

    def delete(self):
        """Delete this roommate and cascade delete bills/chores."""
        CURSOR.execute("DELETE FROM roommates WHERE id=?", (self.id,))
        CONN.commit()

    @classmethod
    def all(cls):
        """Return all roommates."""
        rows = CURSOR.execute("SELECT * FROM roommates").fetchall()
        return [cls(id=row[0], name=row[1], room_number=row[2]) for row in rows]

    @classmethod
    def find_by_id(cls, id: int):
        """Find roommate by ID."""
        row = CURSOR.execute("SELECT * FROM roommates WHERE id=?", (id,)).fetchone()
        return cls(id=row[0], name=row[1], room_number=row[2]) if row else None

    def __repr__(self):
        return f"<Roommate {self.id}: {self.name} (Room {self.room_number})>"