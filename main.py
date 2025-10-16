from lib.database import create_tables
from lib.cli import cli_menu
import click

if __name__ == "__main__":
    #to ensure tables exist before starting CLI
    create_tables()

    # a welcome message
    click.echo("\nWelcome to the Roommate Management System CLI")
    click.echo("Type --help after any command to see usage instructions.\n")

    # Launch CLI
    cli_menu()
