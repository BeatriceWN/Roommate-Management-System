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

"""Bill Commands"""

@cli_menu.command()
def add_bill():
    """Add a new bill, one-time or recurring, and split equally among roommates."""
    name = click.prompt("Bill name").strip()
    if not name:
        click.echo("Bill name cannot be empty.")
        return

    try:
        amount = float(click.prompt("Total amount"))
    except ValueError:
        click.echo("Amount must be a number.")
        return

    due_date = click.prompt("Due date (optional)", default="", show_default=False).strip()
    recurrence_type = click.prompt("Is this a recurring bill? (monthly/none)", default="none").lower().strip()
    recurrence_day = None

    if recurrence_type == "monthly":
        try:
            recurrence_day = int(click.prompt("Enter day of month due (1-31)"))
            if not (1 <= recurrence_day <= 31):
                raise ValueError
        except ValueError:
            click.echo("Day of month must be an integer between 1 and 31.")
            return

    bill = Bill(
        name=name,
        amount=amount,
        due_date=due_date or None,
        recurrence_type=recurrence_type if recurrence_type != "none" else None,
        recurrence_day=recurrence_day
    )
    bill.save()

    try:
        share = bill.split_among_roommates()
        click.echo(f"Bill '{bill.name}' added and split equally: each roommate owes {share}.")
    except ValueError as e:
        click.echo(f"{e}")

@cli_menu.command()
def view_bills():
    """View all bills and roommate payment statuses"""
    bills = Bill.all()
    if not bills:
        click.echo("No bills found.")
        return

    click.echo("\nBills Overview:")
    for bill in bills:
        click.echo(f"\nBill ID {bill.id}: {bill.name} | Amount: {bill.amount} | Due: {bill.due_date or 'N/A'}")
        roommate_bills = RoommateBill.all_for_bill(bill.id)
        if not roommate_bills:
            click.echo("   No roommates assigned to this bill.")
            continue

        for rb in roommate_bills:
            roommate = Roommate.find_by_id(rb.roommate_id)
            roommate_name = roommate.name if roommate else "Unknown"
            click.echo(f"   - {roommate_name}: {rb.share} ({rb.status})")        

@cli_menu.command()
def mark_bill():
    """Mark a roommate's bill as paid or pending"""
    try:
        roommate_id = int(click.prompt("Roommate ID"))
        bill_id = int(click.prompt("Bill ID"))
    except ValueError:
        click.echo("IDs must be numeric.")
        return

    rb = RoommateBill.find_by_roommate_and_bill(roommate_id, bill_id)
    if not rb:
        click.echo(f"No bill found for roommate ID {roommate_id} with bill ID {bill_id}.")
        return

    status = click.prompt(
        "New status (paid/pending)",
        type=click.Choice(["paid", "pending"], case_sensitive=False)
    )

    RoommateBill.update_status(roommate_id, bill_id, status.lower())
    click.echo(f"Updated bill ID {bill_id} for roommate ID {roommate_id} to '{status.lower()}'.")

@cli_menu.command()
def summary():
    """Show system overview"""
    roommates = Roommate.all()
    chores = Chore.all()
    bills = Bill.all()

    click.echo("Roommate Management System Summary\n")
    
    click.echo(f"Total Roommates: {len(roommates)}")
    if roommates:
        for r in roommates:
            click.echo(f" - ID {r.id}: {r.name} | Room: {r.room_number}")
    else:
        click.echo("No roommates registered.\n")

    click.echo(f"\nTotal Chores: {len(chores)}")
    if chores:
        for c in chores:
            roommate = Roommate.find_by_id(c.roommate_id)
            roommate_name = roommate.name if roommate else "Unassigned"
            click.echo(f" - ID {c.id}: {c.title} | Assigned to: {roommate_name} | Status: {'complete' if c.completed else 'pending'}")
    else:
        click.echo("No chores registered.\n")

    click.echo(f"\nTotal Bills: {len(bills)}")
    if bills:
        for bill in bills:
            roommate_bills = RoommateBill.all_for_bill(bill.id)
            total_shares = sum(rb.share for rb in roommate_bills) if roommate_bills else 0
            click.echo(f"\nBill ID {bill.id}: {bill.name} | Amount: {bill.amount} | Due: {bill.due_date or 'N/A'} | Total Collected: {total_shares}")
            if roommate_bills:
                for rb in roommate_bills:
                    roommate = Roommate.find_by_id(rb.roommate_id)
                    roommate_name = roommate.name if roommate else "Unknown"
                    click.echo(f"   - {roommate_name}: {rb.share} ({rb.status})")
            else:
                click.echo("   No roommates assigned to this bill.")
    else:
        click.echo("No bills registered.\n")

    total_due = sum(rb.share for bill in bills for rb in RoommateBill.all_for_bill(bill.id))
    click.echo(f"\nTotal Amount Due Across All Roommates: {total_due}")

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