
---

# Roommate Management System CLI
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python Version](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/) 
[![GitHub Repo](https://img.shields.io/badge/GitHub-Repo-blue?logo=github)](https://github.com/BeatriceWN/Roommate-Management-System)

A command-line application for managing roommates, chores, and shared bills.
Built with **Python**, **SQLite**, and **Click**, it helps track responsibilities and payments in a shared living space.


A command-line application for managing roommates, chores, and shared bills.
Built with **Python**, **SQLite**, and **Click**, it helps track responsibilities and payments in a shared living space.

---

## Learning Goals

This project demonstrates proficiency in Python programming, relational databases, and application structure through the following goals:

* Apply Object-Oriented Programming principles to design maintainable code.
* Implement CRUD operations using Python’s built-in `sqlite3` module.
* Design and manage relational database schemas without external ORM libraries.
* Establish and maintain one-to-many and many-to-many relationships between tables.
* Build a modular command-line interface using the `Click` library for smooth user interaction.
* Enforce data integrity and handle input validation within the application.
* Practice version control using Git and GitHub for project tracking and collaboration.

---

## Table of Contents

* [Learning Goals](#learning-goals)
* [Features](#features)
* [Installation](#installation)
* [Usage](#usage)
* [Database Structure](#database-structure)
* [Relationships Explanation](#relationships-explanation)
* [Tech Stack](#tech-stack)
* [Example CLI Interactions](#example-cli-interactions)
* [Author](#author)
* [License](#license)

---

## Features

### Roommate Management

* Add, view, and delete roommates
* Each roommate has a unique room number

### Chore Tracking

* Assign chores to roommates
* Mark chores as complete or pending
* View all chores and their statuses

### Bill Management

* Add and view bills with optional recurrence details
* Split bills equally among roommates automatically or manually
* Track payment statuses per roommate
* Delete bills and their related records safely

---

## Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/BeatriceWN/Roommate-Management-System
   cd Roommate-Management-System
   ```

2. **Create and activate a virtual environment**

   ```bash
   python -m venv venv
   source venv/bin/activate   # macOS/Linux
   venv\Scripts\activate      # Windows
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**

   ```bash
   python main.py
   ```

---

## Usage

After running `python main.py`, you will see:

```
Welcome to the Roommate Management System CLI
Type --help after any command to see usage instructions.
```

### Roommate Commands

```bash
python main.py add-roommate
python main.py view-roommates
python main.py delete-roommate
```

### Chore Commands

```bash
python main.py add-chore
python main.py view-chores
python main.py mark-chore
python main.py delete-chore
```

### Bill Commands

```bash
python main.py add-bill
python main.py view-bills
python main.py delete-bill
python main.py split-bill
python main.py view-bill-details
python main.py update-bill-status
```

Use `--help` with any command to view its options.
Example:

```bash
python main.py add-bill --help
```

---

## Database Structure

The application uses SQLite, stored in `db/database.db`.
Tables include:

* `roommates`
* `chores`
* `bills`
* `roommate_bills`

Foreign keys ensure relational integrity between roommates, chores, and bills.

---

## Relationships Explanation

* A **Roommate** can have multiple **Chores**, forming a one-to-many relationship.
* A **Bill** can be shared among multiple **Roommates**, creating a many-to-many relationship via `roommate_bills`.
* The `roommate_bills` table tracks each person’s share and payment status.
* Deleting a roommate automatically removes related chores and bill entries.
* Deleting a bill also removes linked records in `roommate_bills`.

This design ensures consistent and accurate data handling across all operations.

---

## Tech Stack

* **Python 3.10+**
* **SQLite3**
* **Click** for CLI interface

---

## Example CLI Interactions

### Add a roommate

```
$ python main.py add-roommate
Roommate name: Adelice
Room number: RM02
Roommate 'Adelice' added successfully.
```

### Add a bill with optional recurrence and auto-split

```
$ python main.py add-bill
Database tables created or verified successfully.

Bill name: WiFi
Total amount: 5000
Due date (YYYY-MM-DD): 2025-10-25
Recurrence type (optional, choose from: daily, weekly, monthly, yearly) []: monthly
Recurrence day (1-31, optional): 27
Bill 'WiFi' added successfully with ID 2.

Do you want to split this bill among all roommates now? (yes/no) [yes]: yes
Bill 'WiFi' split successfully. Each roommate owes 1250.0.
```

### Split an existing bill later

```
$ python main.py split-bill
Bill ID: 2
Bill 'Electricity' split successfully. Each roommate owes 1000.0.
```

### View all bills

```
$ python main.py view-bills
Bills List:
 - ID 1: Rent | Amount: 150000 | Due: 2025-10-30
 - ID 2: WiFi | Amount: 5000 | Due: 2025-10-25
```

### View details of a bill with roommate shares

```
$ python main.py view-bill-details
Bill ID: 1

Bill 'Rent' Details:
 - Alice: 50000.0 (pending)
 - Bob: 50000.0 (paid)
 - Carol: 50000.0 (pending)
```

### Update a roommate's payment status

```
$ python main.py update-bill-status
Roommate ID: 1
Bill ID: 1
New status ('paid' or 'pending'): paid
Updated payment status to 'paid' for roommate ID 1, bill ID 1.
```

---

## Author

**Beatrice Wambui**
Software developer passionate about building efficient CLI and database-driven tools.

GitHub: [github.com/BeatriceWN/Roommate-Management-System](https://github.com/BeatriceWN/Roommate-Management-System)

---

## License

This project is licensed under the **MIT License**.
You are free to use, modify, and distribute this software for personal or commercial purposes, provided that proper credit is given to the original author.

---
