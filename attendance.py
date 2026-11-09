"""
attendance.py
Purpose: Mark attendance (Present / Absent / Leave) for today's date,
view records of one employee, view records of one date, and count days.
Each record looks like: {"employee_id": "EMP001", "date": "2025-01-31", "status": "Present"}
"""

from storage import EMPLOYEES_FILE, ATTENDANCE_FILE, load_data, save_data
from helpers import (print_heading, print_line, ask_valid, today_string,
                     is_valid_date)
from employee import ask_for_employee, find_employee_by_id

STATUS_OPTIONS = {"1": "Present", "2": "Absent", "3": "Leave"}


def get_record_date(record):
    """Used to sort records by date."""
    return record["date"]


def already_marked(attendance, employee_id, date_text):
    """True if this employee already has a record for this date."""
    for record in attendance:
        if record["employee_id"] == employee_id and record["date"] == date_text:
            return True
    return False


def count_days(records):
    """Return (present, absent, leave) totals for a list of records."""
    present = 0
    absent = 0
    leave = 0
    for record in records:
        if record["status"] == "Present":
            present += 1
        elif record["status"] == "Absent":
            absent += 1
        elif record["status"] == "Leave":
            leave += 1
    return present, absent, leave


def mark_attendance():
    print_heading("MARK ATTENDANCE")
    employees = load_data(EMPLOYEES_FILE)
    employee = ask_for_employee(employees)
    if employee is None:
        return

    attendance = load_data(ATTENDANCE_FILE)
    today = today_string()    # the current date is recorded automatically

    if already_marked(attendance, employee["employee_id"], today):
        print(f"Attendance for {employee['name']} is already marked for {today}.")
        return

    print(f"\nEmployee: {employee['name']}    Date: {today}")
    print("1. Present")
    print("2. Absent")
    print("3. Leave")

    while True:
        choice = input("Choose status (1-3): ").strip()
        if choice in STATUS_OPTIONS:
            break
        print("Error: please enter 1, 2 or 3.")

    new_record = {
        "employee_id": employee["employee_id"],
        "date": today,
        "status": STATUS_OPTIONS[choice],
    }
    attendance.append(new_record)
    if save_data(ATTENDANCE_FILE, attendance):
        print(f"Attendance marked: {employee['name']} - {STATUS_OPTIONS[choice]} ({today})")


def view_employee_attendance():
    print_heading("ATTENDANCE OF ONE EMPLOYEE")
    employees = load_data(EMPLOYEES_FILE)
    employee = ask_for_employee(employees)
    if employee is None:
        return

    attendance = load_data(ATTENDANCE_FILE)
    records = []
    for record in attendance:
        if record["employee_id"] == employee["employee_id"]:
            records.append(record)

    print(f"\nAttendance for {employee['name']} ({employee['employee_id']})")
    if len(records) == 0:
        print("No attendance records found for this employee.")
        return

    print_line()
    print(f"{'Date':<15}{'Status'}")
    print_line()
    for record in sorted(records, key=get_record_date):
        print(f"{record['date']:<15}{record['status']}")
    print_line()

    present, absent, leave = count_days(records)
    print("Total Present days :", present)
    print("Total Absent days  :", absent)
    print("Total Leave days   :", leave)


def view_attendance_by_date():
    print_heading("ATTENDANCE ON A DATE")
    # Pressing Enter chooses today's date.
    date_text = ask_valid("Date (YYYY-MM-DD)", is_valid_date,
                          "Enter a real date like 2025-01-31.", today_string())

    attendance = load_data(ATTENDANCE_FILE)
    employees = load_data(EMPLOYEES_FILE)

    records = []
    for record in attendance:
        if record["date"] == date_text:
            records.append(record)

    print(f"\nAttendance on {date_text}")
    if len(records) == 0:
        print("No attendance records found for this date.")
        return

    print_line()
    print(f"{'ID':<10}{'Name':<25}{'Status'}")
    print_line()
    for record in records:
        employee = find_employee_by_id(employees, record["employee_id"])
        if employee is None:
            name = "(unknown)"
        else:
            name = employee["name"]
        print(f"{record['employee_id']:<10}{name[:23]:<25}{record['status']}")
    print_line()

    present, absent, leave = count_days(records)
    print(f"Present: {present}   Absent: {absent}   Leave: {leave}")


def attendance_menu():
    while True:
        print_heading("ATTENDANCE MANAGEMENT")
        print("1. Mark Attendance (today)")
        print("2. View Attendance of an Employee (with totals)")
        print("3. View Attendance of a Date")
        print("4. Back to Main Menu")
        choice = input("\nEnter your choice: ").strip()

        if choice == "1":
            mark_attendance()
        elif choice == "2":
            view_employee_attendance()
        elif choice == "3":
            view_attendance_by_date()
        elif choice == "4":
            break
        else:
            print("Invalid choice. Please enter a number from 1 to 4.")
