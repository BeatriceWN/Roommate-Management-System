import click
from lib.models.roommate import Roommate
from lib.models.chore import Chore
from lib.models.bills import Bill
from lib.models.roommate_bill import RoommateBill
from lib.database import create_tables

VALID_RECURRENCE_TYPES = ["daily", "weekly", "monthly", "yearly"]

@click.group()
def cli_menu():
    """Roommate Management System CLI"""
    create_tables()

""" Roommate Commands """

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
    except Exception as e:
        click.echo(f"Error: {e}")

@cli_menu.command()
def view_roommates():
    """View all roommates"""
    roommates = Roommate.all()
    if not roommates:
        click.echo("No roommates found.")
        return

    click.echo("Roommates List:")
    for r in roommates:
        click.echo(f" - ID {r.id}: {r.name} (Room {r.room_number})")

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

""" Chore Commands """

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
        click.echo(f"Chore '{title}' assigned to '{roommate.name}'.")
    except Exception as e:
        click.echo(f"Error: {e}")

@cli_menu.command()
def view_chores():
    """View all chores"""
    chores = Chore.all()
    if not chores:
        click.echo("No chores found.")
        return

    click.echo("Chore List:")
    for c in chores:
        roommate = Roommate.find_by_id(c.roommate_id)
        roommate_name = roommate.name if roommate else "Unassigned"
        status = "Complete" if c.completed else "Pending"
        click.echo(f" - ID {c.id}: {c.title} | Assigned to: {roommate_name} | Status: {status}")

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

""" Bill Commands """

@cli_menu.command()
@click.option('--name', prompt='Bill name')
@click.option('--amount', prompt='Total amount', type=float)
@click.option('--due_date', prompt='Due date (YYYY-MM-DD)', required=False)
@click.option('--recurrence_type', prompt=f"Recurrence type (optional, choose from: {', '.join(VALID_RECURRENCE_TYPES)})", default="", show_default=False)
@click.option('--recurrence_day', prompt='Recurrence day (1-31, optional)', type=int, required=False)
def add_bill(name, amount, due_date, recurrence_type, recurrence_day):
    """Add a new bill"""
    recurrence_type = recurrence_type.strip() or None
    if recurrence_type and recurrence_type not in VALID_RECURRENCE_TYPES:
        click.echo(f"Invalid recurrence type. Choose from: {', '.join(VALID_RECURRENCE_TYPES)}")
        return

    try:
        bill = Bill(
            name=name.strip(),
            amount=amount,
            due_date=due_date,
            recurrence_type=recurrence_type,
            recurrence_day=recurrence_day
        )
        bill.save()
        click.echo(f"Bill '{bill.name}' added successfully with ID {bill.id}.")

        # Auto split prompt
        roommates = Roommate.all()
        if roommates:
            split_choice = click.prompt(
                "Do you want to split this bill among all roommates now? (yes/no)",
                default="yes"
            ).strip().lower()

            if split_choice in ['yes', 'y']:
                share = bill.split_among_roommates()
                click.echo(f"Bill '{bill.name}' split successfully. Each roommate owes {share}.")
            else:
                click.echo("Bill not split. You can split it later using the 'split-bill' command.")
        else:
            click.echo("No roommates found. Cannot split the bill.")

    except Exception as e:
        click.echo(f"Error: {e}")

@cli_menu.command()
def view_bills():
    """View all bills"""
    bills = Bill.all()
    if not bills:
        click.echo("No bills found.")
        return

    click.echo("Bills List:")
    for b in bills:
        click.echo(f" - ID {b.id}: {b.name} | Amount: {b.amount} | Due: {b.due_date or 'N/A'}")

@cli_menu.command()
@click.option('--id', prompt='Bill ID', type=int)
def delete_bill(id):
    """Delete a bill"""
    bill = Bill.find_by_id(id)
    if not bill:
        click.echo(f"No bill found with ID {id}.")
        return

    bill.delete()
    click.echo(f"Deleted bill '{bill.name}' successfully.")

@cli_menu.command()
@click.option('--bill_id', prompt='Bill ID', type=int)
def split_bill(bill_id):
    """Split a bill equally among all roommates."""
    bill = Bill.find_by_id(bill_id)
    if not bill:
        click.echo(f"No bill found with ID {bill_id}.")
        return

    roommates = Roommate.all()
    if not roommates:
        click.echo("No roommates found. Cannot split the bill.")
        return

    try:
        share = bill.split_among_roommates()
        click.echo(f"Bill '{bill.name}' split successfully. Each roommate owes {share}.")
    except Exception as e:
        click.echo(f"Error: {e}")

@cli_menu.command()
@click.option('--bill_id', prompt='Bill ID', type=int)
def view_bill_details(bill_id):
    """View roommate shares for a bill"""
    bill = Bill.find_by_id(bill_id)
    if not bill:
        click.echo(f"No bill found with ID {bill_id}.")
        return

    shares = RoommateBill.all_for_bill(bill_id)
    if not shares:
        click.echo(f"No roommate shares found for bill '{bill.name}'.")
        return

    click.echo(f"Bill '{bill.name}' Details:")
    for s in shares:
        roommate = Roommate.find_by_id(s.roommate_id)
        click.echo(f" - {roommate.name if roommate else 'Unknown'}: {s.share} ({s.status})")

@cli_menu.command()
@click.option('--roommate_id', prompt='Roommate ID', type=int)
@click.option('--bill_id', prompt='Bill ID', type=int)
@click.option('--status', prompt="New status ('paid' or 'pending')")
def update_bill_status(roommate_id, bill_id, status):
    """Update a roommate's payment status for a bill"""
    try:
        RoommateBill.update_status(roommate_id, bill_id, status.strip().lower())
        click.echo(f"Updated payment status to '{status}' for roommate ID {roommate_id}, bill ID {bill_id}.")
    except Exception as e:
        click.echo(f"Error: {e}")

""" Entry Point """
if __name__ == "__main__":
    cli_menu()