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
