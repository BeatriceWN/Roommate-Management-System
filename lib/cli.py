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

"""Chore Commands"""

@cli_menu.command()
@click.option('--title', prompt='Chore title')
@click.option('--roommate_id', prompt='Assign to roommate ID', type=int)
def add_chore(title, roommate_id):
    """Add a new chore"""
    title = title.strip()
    if not title:
        click.echo("Chore title cannot be empty.")
        return

    roommate = Roommate.find_by_id(roommate_id)
    if not roommate:
        click.echo(f"No roommate found with ID {roommate_id}.")
        return

    try:
        chore = Chore(title=title, roommate_id=roommate_id)
        chore.save()
        click.echo(f"Chore '{title}' added to roommate '{roommate.name}'.")
    except ValueError as e:
        click.echo(f"Error: {e}")    

@cli_menu.command()
def view_chores():
    """View all chores"""
    chores = Chore.all()
    if not chores:
        click.echo("No chores found.")
        return

    click.echo("\n🧹 Chore List:")
    for c in chores:
        roommate = Roommate.find_by_id(c.roommate_id)
        roommate_name = roommate.name if roommate else "Unassigned"
        click.echo(f" - ID {c.id}: {c.title} | Assigned to: {roommate_name} | Status: {'complete' if c.completed else 'pending'}")

@cli_menu.command()
@click.option('--id', prompt='Chore ID', type=int)
@click.option('--done', prompt='Mark complete? (yes/no)')
def mark_chore(id, done):
    """Mark a chore as complete or pending"""
    chore = Chore.find_by_id(id)
    if not chore:
        click.echo(f"No chore found with ID {id}.")
        return

    done_clean = done.strip().lower()
    if done_clean not in ['yes', 'y', 'no', 'n']:
        click.echo("Invalid input. Please enter 'yes' or 'no'.")
        return

    chore.update_status(done_clean in ['yes', 'y'])
    click.echo(f"Chore '{chore.title}' marked as {'complete' if chore.completed else 'pending'}.")

@cli_menu.command()
@click.option('--id', prompt='Chore ID', type=int)
def delete_chore(id):
    """Delete a chore"""
    chore = Chore.find_by_id(id)
    if not chore:
        click.echo(f"No chore found with ID {id}.")
        return

    chore.delete()
    click.echo(f"Deleted chore '{chore.title}' successfully.")   
