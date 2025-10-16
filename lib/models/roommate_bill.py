from lib.database import CURSOR, CONN

class RoommateBill:
    VALID_STATUSES = ["pending", "paid"]

    def __init__(self, roommate_id, bill_id, share, status="pending", id=None):
        if status not in self.VALID_STATUSES:
            raise ValueError(f"Status must be one of {self.VALID_STATUSES}")
        self.id = id
        self.roommate_id = roommate_id
        self.bill_id = bill_id
        self.share = share
        self.status = status

    def save(self):
        existing = CURSOR.execute(
            "SELECT id FROM roommate_bills WHERE roommate_id=? AND bill_id=?",
            (self.roommate_id, self.bill_id)
        ).fetchone()
        if existing:
            self.id = existing[0]
            return self

        CURSOR.execute(
            "INSERT INTO roommate_bills (roommate_id, bill_id, share, status) VALUES (?, ?, ?, ?)",
            (self.roommate_id, self.bill_id, self.share, self.status)
        )
        CONN.commit()
        self.id = CURSOR.lastrowid
        return self
