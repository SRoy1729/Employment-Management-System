# Employment Management System

A console-based (command line) application, written in beginner-level Python 3, that lets an administrator manage employees, salaries, departments and attendance. All data is stored permanently in JSON files.

This is a BCA college project. It uses only Python's built-in modules (`json`, `os`, `datetime`), so nothing needs to be installed.

## Project Objectives

- Practise basic Python: variables, lists, dictionaries, if-else, loops, functions, file handling and exception handling.
- Store data permanently using JSON files.
- Build a clean, menu-driven program that does not crash on ordinary wrong input.
- Organise code into small, readable files, each with one job.

## Features

1. **Add Employee** - automatic unique ID (EMP001, EMP002, ...), input validation, no empty mandatory fields.
2. **View Employee Records** - summary table, full details of everyone, or one employee.
3. **Update Employee Details** - press Enter to keep an old value; the Employee ID never changes.
4. **Delete Employee** - shows details, asks for confirmation, also removes that employee's attendance records.
5. **Search Employee** - by ID, name (partial), department or job position.
6. **Salary Management** - view salaries, search by ID, update basic salary, monthly and annual salary (monthly x 12). Negative values are rejected.
7. **Department Management** - add, view, search, rename, delete (only when no employee is assigned). Duplicates are blocked.
8. **Attendance Management** - mark Present / Absent / Leave for today, view by employee (with totals) or by date, no duplicate entries for the same day.
9. **Exit** - closes the program safely.

## Technologies Used

- Python 3 (tested with Python 3.12; any recent Python 3 should work)
- Built-in modules only: `json`, `os`, `datetime`
- VS Code, Git and GitHub

## Project Folder Structure

```
Employment-Management-System/
├── main.py          # starts the program, shows the main menu
├── employee.py      # add, view, update, delete, search employees
├── department.py    # department management
├── salary.py        # salary management
├── attendance.py    # attendance management
├── storage.py       # reads and writes the JSON files
├── helpers.py       # input checking, headings, money formatting
├── data/
│   ├── employees.json     # created automatically
│   ├── departments.json   # created automatically
│   └── attendance.json    # created automatically
├── README.md
└── .gitignore
```

## Installation

1. Install Python 3 from https://www.python.org/downloads/ (tick "Add Python to PATH" on Windows).
2. Download or clone this project.

## How to Run

```
cd Employment-Management-System
python main.py
```

(On some systems use `python3 main.py`.) The `data` folder and JSON files are created automatically on first run.

## Example Console Output

```
============================================================
                EMPLOYMENT MANAGEMENT SYSTEM
============================================================
1. Add Employee
2. View Employee Records
3. Update Employee Details
4. Delete Employee
5. Search Employee
6. Salary Management
7. Department Management
8. Attendance Management
9. Exit
============================================================
Enter your choice: 2

ID      Name                  Department        Position                     Salary
------------------------------------------------------------------------------------
EMP001  Subir Roy              IT              Data Analyst             Rs. 92,000.00

Total employees: 1
```

## Future Improvements

- Administrator login with a password
- Export reports to CSV
- Monthly attendance report
- Search employees by joining date
- A graphical or web interface

## Author

Your Name - Swagata Roy
date: 09/11/2026
