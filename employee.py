"""
employee.py
Purpose: Add, view, update, delete and search employees.
It also provides find_employee_by_id() and ask_for_employee(),
which salary.py and attendance.py reuse.
"""

from storage import (EMPLOYEES_FILE, DEPARTMENTS_FILE, ATTENDANCE_FILE,
                     load_data, save_data)
from helpers import (print_heading, print_line, format_money, ask_valid,
                     ask_yes_no, is_not_empty, is_valid_age, is_valid_gender,
                     is_valid_phone, is_valid_email, is_valid_joining_date,
                     is_valid_salary)
from department import choose_department


# ---------------------------------------------------------------
# Small helper functions
# ---------------------------------------------------------------
def find_employee_by_id(employees, employee_id):
    """Return the employee dictionary with this ID, or None if not found."""
    employee_id = employee_id.strip().upper()
    for employee in employees:
        if employee["employee_id"].upper() == employee_id:
            return employee
    return None


def ask_for_employee(employees):
    """Ask for an Employee ID. Returns the employee, or None (with a message)."""
    if len(employees) == 0:
        print("No employees are registered yet.")
        return None

    employee_id = input("Enter Employee ID (example: EMP001): ").strip()
    employee = find_employee_by_id(employees, employee_id)
    if employee is None:
        print("Error: no employee found with ID '" + employee_id + "'.")
    return employee


def generate_employee_id(employees):
    """Create the next ID: EMP001, EMP002, ... (never repeats an existing ID)."""
    highest_number = 0
    for employee in employees:
        number_part = employee["employee_id"][3:]
        if number_part.isdecimal() and int(number_part) > highest_number:
            highest_number = int(number_part)

    new_number = highest_number + 1
    new_id = f"EMP{new_number:03d}"

    # Extra safety: make sure the ID is really unique.
    while find_employee_by_id(employees, new_id) is not None:
        new_number += 1
        new_id = f"EMP{new_number:03d}"
    return new_id


def print_employee_table(employee_list):
    """Print employees as a table: ID, name, department, position, salary."""
    print(f"{'ID':<8}{'Name':<22}{'Department':<18}{'Position':<20}{'Salary':>16}")
    print("-" * 84)
    for employee in employee_list:
        print(f"{employee['employee_id']:<8}"
              f"{employee['name'][:20]:<22}"
              f"{employee['department'][:16]:<18}"
              f"{employee['position'][:18]:<20}"
              f"{format_money(employee['basic_salary']):>16}")


def print_employee_details(employee):
    """Print every detail of one employee."""
    print_line()
    print("Employee ID    :", employee["employee_id"])
    print("Name           :", employee["name"])
    print("Age            :", employee["age"])
    print("Gender         :", employee["gender"])
    print("Phone          :", employee["phone"])
    print("Email          :", employee["email"])
    print("Address        :", employee["address"])
    print("Department     :", employee["department"])
    print("Position       :", employee["position"])
    print("Joining Date   :", employee["joining_date"])
    print("Basic Salary   :", format_money(employee["basic_salary"]))
    print_line()


# ---------------------------------------------------------------
# Module 1: Add Employee
# ---------------------------------------------------------------
def add_employee():
    print_heading("ADD NEW EMPLOYEE")
    employees = load_data(EMPLOYEES_FILE)
    departments = load_data(DEPARTMENTS_FILE)

    if len(departments) == 0:
        print("No departments exist. Please add a department first")
        print("(Main Menu -> Department Management).")
        return

    new_id = generate_employee_id(employees)
    print("Employee ID (automatic):", new_id)

    name = ask_valid("Name", is_not_empty, "Name cannot be empty.")
    age = ask_valid("Age (18-70)", is_valid_age, "Enter a whole number from 18 to 70.")
    gender = ask_valid("Gender (Male/Female/Other)", is_valid_gender,
                       "Type Male, Female or Other.")
    phone = ask_valid("Phone number (digits only)", is_valid_phone,
                      "Enter 10 to 15 digits, no spaces or symbols.")
    email = ask_valid("Email address", is_valid_email,
                      "Enter a valid email, e.g. name@example.com.")
    address = ask_valid("Address", is_not_empty, "Address cannot be empty.")
    department = choose_department()
    position = ask_valid("Job position", is_not_empty, "Position cannot be empty.")
    joining_date = ask_valid("Joining date (YYYY-MM-DD)", is_valid_joining_date,
                             "Enter a real date, not in the future, like 2025-01-31.")
    salary = ask_valid("Basic monthly salary", is_valid_salary,
                       "Enter a number greater than 0.")

    new_employee = {
        "employee_id": new_id,
        "name": name,
        "age": int(age),
        "gender": gender.capitalize(),
        "phone": phone,
        "email": email,
        "address": address,
        "department": department,
        "position": position,
        "joining_date": joining_date,
        "basic_salary": float(salary),
    }

    employees.append(new_employee)
    if save_data(EMPLOYEES_FILE, employees):
        print(f"\nEmployee {name} added successfully with ID {new_id}.")


# ---------------------------------------------------------------
# Module 2: View Employee Records
# ---------------------------------------------------------------
def view_employees():
    while True:
        print_heading("VIEW EMPLOYEE RECORDS")
        print("1. Summary table of all employees")
        print("2. Complete details of all employees")
        print("3. Complete details of one employee")
        print("4. Back to Main Menu")
        choice = input("\nEnter your choice: ").strip()

        if choice == "4":
            break
        if choice not in ["1", "2", "3"]:
            print("Invalid choice. Please enter a number from 1 to 4.")
            continue

        employees = load_data(EMPLOYEES_FILE)
        if len(employees) == 0:
            print("No employees are registered yet.")
        elif choice == "1":
            print()
            print_employee_table(employees)
            print(f"\nTotal employees: {len(employees)}")
        elif choice == "2":
            for employee in employees:
                print_employee_details(employee)
        else:
            employee = ask_for_employee(employees)
            if employee is not None:
                print_employee_details(employee)


# ---------------------------------------------------------------
# Module 3: Update Employee Details
# ---------------------------------------------------------------
def update_employee():
    print_heading("UPDATE EMPLOYEE DETAILS")
    employees = load_data(EMPLOYEES_FILE)
    employee = ask_for_employee(employees)
    if employee is None:
        return

    print("\nCurrent details:")
    print_employee_details(employee)
    print("Type a new value, or just press Enter to keep the old one.")
    print("(The Employee ID cannot be changed.)\n")

    # The old value is passed in, so pressing Enter keeps it.
    employee["name"] = ask_valid("Name", is_not_empty, "Name cannot be empty.",
                                 employee["name"])
    employee["age"] = int(ask_valid("Age (18-70)", is_valid_age,
                                    "Enter a whole number from 18 to 70.",
                                    employee["age"]))
    employee["gender"] = ask_valid("Gender", is_valid_gender,
                                   "Type Male, Female or Other.",
                                   employee["gender"]).capitalize()
    employee["phone"] = ask_valid("Phone", is_valid_phone,
                                  "Enter 10 to 15 digits.", employee["phone"])
    employee["email"] = ask_valid("Email", is_valid_email,
                                  "Enter a valid email.", employee["email"])
    employee["address"] = ask_valid("Address", is_not_empty,
                                    "Address cannot be empty.", employee["address"])
    employee["department"] = choose_department(employee["department"])
    employee["position"] = ask_valid("Position", is_not_empty,
                                     "Position cannot be empty.", employee["position"])
    employee["joining_date"] = ask_valid("Joining date (YYYY-MM-DD)",
                                         is_valid_joining_date,
                                         "Enter a real date, not in the future.",
                                         employee["joining_date"])
    employee["basic_salary"] = float(ask_valid("Basic monthly salary", is_valid_salary,
                                               "Enter a number greater than 0.",
                                               employee["basic_salary"]))

    # 'employee' is the same dictionary that sits inside the 'employees' list,
    # so saving the list saves the changes. Other employees stay untouched.
    if save_data(EMPLOYEES_FILE, employees):
        print("\nEmployee details updated successfully.")


# ---------------------------------------------------------------
# Module 4: Delete Employee
# ---------------------------------------------------------------
def delete_employee():
    print_heading("DELETE EMPLOYEE")
    employees = load_data(EMPLOYEES_FILE)
    employee = ask_for_employee(employees)
    if employee is None:
        return

    print_employee_details(employee)
    if not ask_yes_no("Are you sure you want to delete this employee?"):
        print("Deletion cancelled.")
        return

    employees.remove(employee)
    save_data(EMPLOYEES_FILE, employees)

    # Also remove this employee's attendance records, so no orphan records remain.
    attendance = load_data(ATTENDANCE_FILE)
    remaining_records = []
    for record in attendance:
        if record["employee_id"] != employee["employee_id"]:
            remaining_records.append(record)
    removed_count = len(attendance) - len(remaining_records)
    save_data(ATTENDANCE_FILE, remaining_records)

    print("Employee deleted successfully.")
    print(f"Attendance records removed: {removed_count}")


# ---------------------------------------------------------------
# Module 5: Search Employee
# ---------------------------------------------------------------
def search_by_text(employees, field_name, text):
    """Return employees whose field contains the text (partial, any case)."""
    matches = []
    for employee in employees:
        if text.lower() in employee[field_name].lower():
            matches.append(employee)
    return matches


def show_search_results(matches):
    if len(matches) == 0:
        print("No matching employee found.")
    else:
        print(f"\n{len(matches)} employee(s) found:\n")
        print_employee_table(matches)


def search_employee():
    while True:
        print_heading("SEARCH EMPLOYEE")
        print("1. Search by Employee ID")
        print("2. Search by Name (partial allowed)")
        print("3. Search by Department")
        print("4. Search by Job Position")
        print("5. Back to Main Menu")
        choice = input("\nEnter your choice: ").strip()

        if choice == "5":
            break
        if choice not in ["1", "2", "3", "4"]:
            print("Invalid choice. Please enter a number from 1 to 5.")
            continue

        employees = load_data(EMPLOYEES_FILE)
        if len(employees) == 0:
            print("No employees are registered yet.")
            continue

        text = ask_valid("Enter search text", is_not_empty,
                         "Search text cannot be empty.")

        if choice == "1":
            employee = find_employee_by_id(employees, text)
            if employee is None:
                print("No matching employee found.")
            else:
                print_employee_details(employee)
        elif choice == "2":
            show_search_results(search_by_text(employees, "name", text))
        elif choice == "3":
            show_search_results(search_by_text(employees, "department", text))
        else:
            show_search_results(search_by_text(employees, "position", text))
