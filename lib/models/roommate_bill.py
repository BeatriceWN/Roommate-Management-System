from lib.database import CURSOR, CONN

class RoommateBill:
    """Links roommates to their share of a bill."""

    VALID_STATUSES = ["pending", "paid"]

    def __init__(self, roommate_id: int, bill_id: int, share: float, status: str = "pending", id: int = None):
        if status not in self.VALID_STATUSES:
            raise ValueError(f"Status must be one of {self.VALID_STATUSES}")
        if share < 0:
            raise ValueError("Share cannot be negative.")

        self.id = id
        self.roommate_id = roommate_id
        self.bill_id = bill_id
        self.share = share
        self.status = status

    def save(self):
        """Save roommate-bill record, preventing duplicates."""
        existing = CURSOR.execute(
            "SELECT id FROM roommate_bills WHERE roommate_id=? AND bill_id=?",
            (self.roommate_id, self.bill_id),
        ).fetchone()

        if existing:
            self.id = existing[0]
            return self

        CURSOR.execute(
            "INSERT INTO roommate_bills (roommate_id, bill_id, share, status) VALUES (?, ?, ?, ?)",
            (self.roommate_id, self.bill_id, self.share, self.status),
        )
        CONN.commit()
        self.id = CURSOR.lastrowid
        return self

    @classmethod
    def update_status(cls, roommate_id: int, bill_id: int, new_status: str):
        """Update payment status for a roommate's share."""
        if new_status not in cls.VALID_STATUSES:
            raise ValueError(f"Status must be one of {cls.VALID_STATUSES}")
        CURSOR.execute(
            "UPDATE roommate_bills SET status=? WHERE roommate_id=? AND bill_id=?",
            (new_status, roommate_id, bill_id),
        )
        CONN.commit()

    @classmethod
    def all_for_bill(cls, bill_id: int):
        """Get all roommate bills for a specific bill."""
        rows = CURSOR.execute("SELECT * FROM roommate_bills WHERE bill_id=?", (bill_id,)).fetchall()
        return [cls(id=row[0], roommate_id=row[1], bill_id=row[2], share=row[3], status=row[4]) for row in rows]

    @classmethod
    def find_by_roommate_and_bill(cls, roommate_id: int, bill_id: int):
        """Find a specific roommate-bill pair."""
        row = CURSOR.execute(
            "SELECT * FROM roommate_bills WHERE roommate_id=? AND bill_id=?",
            (roommate_id, bill_id),
        ).fetchone()
        return cls(id=row[0], roommate_id=row[1], bill_id=row[2], share=row[3], status=row[4]) if row else None

    def delete(self):
        """Delete a roommate-bill record."""
        CURSOR.execute("DELETE FROM roommate_bills WHERE id=?", (self.id,))
        CONN.commit()

    def __repr__(self):
        return f"<RoommateBill {self.id}: Roommate {self.roommate_id} | Bill {self.bill_id} | Share {self.share} | Status {self.status}>"