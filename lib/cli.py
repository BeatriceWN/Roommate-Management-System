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

    @cli_menu.command()

def view_roommates():
    """View all roommates"""
    roommates = Roommate.all()
    if not roommates:
        click.echo("No roommates found.")
        return
    
    click.echo("\n Roommates List:")
    for r in roommates:
        click.echo(f" - {r}")    

@cli_menu.command()
@click.option('--id', prompt='Roommate ID', type=int)
def delete_roommate(id):
    """Delete a roommate"""
    roommate = Roommate.find_by_id(id)
    if not roommate:
        click.echo(f"No roommate found with ID {id}.")
        return

    roommate.delete()
    click.echo(f"Deleted roommate '{roommate.name}' successfully.")