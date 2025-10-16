import click
from lib.models.roommate import Roommate
from lib.models.chore import Chore
from lib.models.bills import Bill
from lib.models.roommate_bill import RoommateBill


@click.group()
def cli_menu():
    """Roommate Management System CLI"""
    pass
