from lib.database import CURSOR, CONN
from lib.models.roommate import Roommate
from lib.models.roommate_bill import RoommateBill

class Bill:
    def __init__(self, name, amount, due_date=None, recurrence_type=None, recurrence_day=None, id=None):
        if not name:
            raise ValueError("Bill name cannot be empty.")
        if amount <= 0:
            raise ValueError("Bill amount must be positive.")
        if recurrence_day and not (1 <= recurrence_day <= 31):
            raise ValueError("Recurrence day must be between 1 and 31.")

        self.id = id
        self.name = name
        self.amount = amount
        self.due_date = due_date
        self.recurrence_type = recurrence_type
        self.recurrence_day = recurrence_day

    def save(self):
        CURSOR.execute(
            "INSERT INTO bills (name, amount, due_date, recurrence_type, recurrence_day) VALUES (?, ?, ?, ?, ?)",
            (self.name, self.amount, self.due_date, self.recurrence_type, self.recurrence_day)
        )
        CONN.commit()
        self.id = CURSOR.lastrowid
        return self

    def update(self):
        CURSOR.execute(
            "UPDATE bills SET name=?, amount=?, due_date=?, recurrence_type=?, recurrence_day=? WHERE id=?",
            (self.name, self.amount, self.due_date, self.recurrence_type, self.recurrence_day, self.id)
        )
        CONN.commit()
    @classmethod
    def all(cls):
        rows = CURSOR.execute("SELECT * FROM bills").fetchall()
        return [
            cls(
                id=row[0],
                name=row[1],
                amount=row[2],
                due_date=row[3],
                recurrence_type=row[4],
                recurrence_day=row[5]
            )
            for row in rows
        ]

    @classmethod
    def find_by_id(cls, id):
        row = CURSOR.execute("SELECT * FROM bills WHERE id = ?", (id,)).fetchone()
        if not row:
            return None
        return cls(
            id=row[0],
            name=row[1],
            amount=row[2],
            due_date=row[3],
            recurrence_type=row[4],
            recurrence_day=row[5]
        )
