````markdown
# Roommate Management System CLI

A command-line application to manage roommates, chores, and bills using Python and SQLite.  
This project demonstrates manual ORM-style classes, CRUD operations, and database interactions without external ORM libraries.

---

##   Installation

1. Clone the repository:

```bash
git clone https://github.com/BeatriceWN/Roommate-Management-System.git
cd Roommate-Management-System
````

2. Create and activate a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate   # macOS/Linux
venv\Scripts\activate      # Windows
```

3. Install dependencies:

```bash
pip install click
```

---

##   Running the Application

1. Launch the CLI:

```bash
python3 main.py
```

2. Available commands:

### Roommates

* Add a roommate: `add-roommate`
* View all roommates: `view-roommates`
* Delete a roommate: `delete-roommate`

### Chores

* Add a chore: `add-chore`
* View all chores: `view-chores`
* Mark chore complete/pending: `mark-chore`
* Delete a chore: `delete-chore`

### Bills

* Add a bill: `add-bill`
* View bills and payments: `view-bills`
* Mark a roommate's bill as paid/pending: `mark-bill`
* Delete a bill: `delete-bill`

### Summary

* View system summary: `summary`

---

##   Example Workflows

### 1. Add Roommates

```bash
$ python3 main.py add-roommate
Roommate name: Beatrice Wambui
Room number: RM1
Roommate 'Beatrice Wambui' added successfully.

$ python3 main.py add-roommate
Roommate name: Nancy Adelice
Room number: RM2
Roommate 'Nancy Adelice' added successfully.

$ python3 main.py add-roommate
Roommate name: Jason Munene
Room number: RM3
Roommate 'Jason Munene' added successfully.

$ python3 main.py add-roommate
Roommate name: Bernice Maria
Room number: RM-4
Roommate 'Bernice Maria' added successfully.

$ python3 main.py add-roommate
Roommate name: Martin King
Room number: RM-5
Roommate 'Martin King' added successfully.
```

### 2. View Roommates

```bash
$ python3 main.py view-roommates
 Roommates List:
 - <Roommate 1: Beatrice Wambui (Room RM1)>
 - <Roommate 2: Nancy Adelice (Room RM2)>
 - <Roommate 3: Jason Munene (Room RM3)>
 - <Roommate 4: Bernice Maria (Room RM-4)>
 - <Roommate 5: Martin King (Room RM-5)>
```

### 3. Delete a Roommate

```bash
$ python3 main.py delete-roommate
Roommate ID: 5
Deleted roommate 'Martin King' successfully.
```

---

### 4. Add a Chore

```bash
$ python3 main.py add-chore
Chore title: Clean kitchen
Assign to roommate ID: 1
  Chore 'Clean kitchen' added to roommate 'Beatrice Wambui'.

$ python3 main.py add-chore
Chore title: Vacuum living room
Assign to roommate ID: 2
  Chore 'Vacuum living room' added to roommate 'Nancy Adelice'.
```

### 5. View Chores

```bash
$ python3 main.py view-chores
  Chore List:
 - ID 1: Clean kitchen | Assigned to: Beatrice Wambui | Status: pending
 - ID 2: Vacuum living room | Assigned to: Nancy Adelice | Status: pending
```

### 6. Mark Chore Complete/Pending

```bash
$ python3 main.py mark-chore
Chore ID: 1
Mark complete? (yes/no): yes
Chore 'Clean kitchen' marked as complete.
```

### 7. Delete a Chore

```bash
$ python3 main.py delete-chore
Chore ID: 2
Deleted chore 'Vacuum living room' successfully.
```

---

### 8. Add a Bill

```bash
$ python3 main.py add-bill
Bill name: Rent
Total amount: 150000
Due date (optional): 2025/10/25
Is this a recurring bill? (monthly/none) [none]: monthly
Enter day of month due (1-31): 25
Bill 'Rent' added and split equally: each roommate owes 30000.0.
```

### 9. View Bills

```bash
$ python3 main.py view-bills

Bill ID 1: Rent | Amount: 150000.0 | Due: 2025/10/25
   - Beatrice Wambui: 30000.0 (pending)
   - Nancy Adelice: 30000.0 (pending)
   - Jason Munene: 30000.0 (pending)
   - Bernice Maria: 30000.0 (pending)
```

### 10. Mark a Bill Paid/Pending

```bash
$ python3 main.py mark-bill
Roommate ID: 1
Bill ID: 1
New status (paid/pending): paid
Updated bill ID 1 for roommate ID 1 to 'paid'.
```

### 11. Delete a Bill

```bash
$ python3 main.py delete-bill
Bill ID: 1
Deleted bill 'Rent' successfully.
```

---

### 12. View System Summary

```bash
$ python3 main.py summary
Roommate Management System Summary

Total Roommates: 4
 - ID 1: Beatrice Wambui | Room: RM1
 - ID 2: Nancy Adelice | Room: RM2
 - ID 3: Jason Munene | Room: RM3
 - ID 4: Bernice Maria | Room: RM-4

Total Chores: 1
 - ID 1: Clean kitchen | Assigned to: Beatrice Wambui | Status: complete

Total Bills: 0

Total Amount Due Across All Roommates: 0
```

---

## Additional Info

* SQLite database file is auto-created in `db/database.db`.
* All models handle their own CRUD operations without external ORM libraries.
* CLI is built using Click for prompts and input handling.

---

## Author

**Beatrice Wambui**
[GitHub](https://github.com/BeatriceWN/Roommate-Management-System)

