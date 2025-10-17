from lib.database import create_tables
from lib.cli import cli_menu

if __name__ == "__main__":
    #ensure database tables are created before starting the CLI
    create_tables()
    
    # Launch the Command-Line Interface
    cli_menu()
