import click
from lib.models.roommate import Roommate
from lib.models.chore import Chore
from lib.models.bills import Bill
from lib.models.roommate_bill import RoommateBill


@click.group()
def cli_menu():
    """Roommate Management System CLI"""
    pass

"""Roommate Commands"""

@cli_menu.command()
@click.option('--name', prompt='Roommate name')
@click.option('--room', prompt='Room number')
def add_roommate(name, room):
    """Add a new roommate"""
    name = name.strip()
    room = room.strip()
    if not name:
        click.echo("Roommate name cannot be empty.")
        return
    if not room:
        click.echo("Room number cannot be empty.")
        return

    try:
        roommate = Roommate(name=name, room_number=room)
        roommate.save()
        click.echo(f"Roommate '{name}' added successfully.")
    except ValueError as e:
        click.echo(f"Error: {e}")