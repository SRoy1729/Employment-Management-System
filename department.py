"""
department.py
Purpose: Everything about departments - add, view, search, rename, delete.
It also provides choose_department(), which employee.py uses so that an
employee can only be placed in a department that really exists.
"""

from storage import (EMPLOYEES_FILE, DEPARTMENTS_FILE,
                     load_data, save_data)
from helpers import print_heading, ask_valid, ask_yes_no, is_not_empty


def clean_name(text):
    """Remove extra spaces: '  Human   Resources ' -> 'Human Resources'."""
    return " ".join(text.split())


def find_department(departments, name):
    """Find a department ignoring upper/lower case. Returns the stored name or None."""
    for department in departments:
        if department.lower() == name.lower():
            return department
    return None


def choose_department(current_department=None):
    """
    Show a numbered list and let the user pick one by number.
    Returns the department name.
    When updating, pressing Enter keeps current_department.
    """
    departments = load_data(DEPARTMENTS_FILE)
    if len(departments) == 0:
        return current_department

    print("\nAvailable departments:")
    for number, name in enumerate(departments, start=1):
        print(f"  {number}. {name}")

    prompt = "Choose department number"
    if current_department is not None:
        prompt += f" [{current_department}] (Enter to keep)"

    while True:
        text = input(prompt + ": ").strip()
        if text == "" and current_department is not None:
            return current_department
        if text.isdecimal() and 1 <= int(text) <= len(departments):
            return departments[int(text) - 1]
        print("Error: please enter a number from the list.")


def add_department():
    print_heading("ADD DEPARTMENT")
    departments = load_data(DEPARTMENTS_FILE)

    name = ask_valid("New department name", is_not_empty, "Name cannot be empty.")
    name = clean_name(name)

    if find_department(departments, name) is not None:
        print("Error: that department already exists.")
        return

    departments.append(name)
    save_data(DEPARTMENTS_FILE, departments)
    print(f"Department '{name}' added successfully.")


def view_departments():
    print_heading("ALL DEPARTMENTS")
    departments = load_data(DEPARTMENTS_FILE)

    if len(departments) == 0:
        print("No departments found.")
        return

    for number, name in enumerate(departments, start=1):
        print(f"  {number}. {name}")


def search_department():
    print_heading("SEARCH DEPARTMENT")
    departments = load_data(DEPARTMENTS_FILE)
    text = ask_valid("Enter part of the department name", is_not_empty,
                     "Search text cannot be empty.")

    found = False
    for name in departments:
        if text.lower() in name.lower():
            print("  -", name)
            found = True

    if not found:
        print("No matching department found.")


def rename_department():
    print_heading("RENAME DEPARTMENT")
    departments = load_data(DEPARTMENTS_FILE)

    old_input = ask_valid("Current department name", is_not_empty,
                          "Name cannot be empty.")
    old_name = find_department(departments, clean_name(old_input))
    if old_name is None:
        print("Error: department not found.")
        return

    new_input = ask_valid("New department name", is_not_empty,
                          "Name cannot be empty.")
    new_name = clean_name(new_input)

    # Block duplicates (but allow changing only the capital letters of the same name).
    existing = find_department(departments, new_name)
    if existing is not None and existing.lower() != old_name.lower():
        print("Error: a department with that name already exists.")
        return

    # Replace the name in the departments list.
    position = departments.index(old_name)
    departments[position] = new_name
    save_data(DEPARTMENTS_FILE, departments)

    # Employees store the department name, so update them too.
    employees = load_data(EMPLOYEES_FILE)
    changed = 0
    for employee in employees:
        if employee["department"].lower() == old_name.lower():
            employee["department"] = new_name
            changed += 1
    save_data(EMPLOYEES_FILE, employees)

    print(f"Department renamed to '{new_name}'. Employees updated: {changed}")


def delete_department():
    print_heading("DELETE DEPARTMENT")
    departments = load_data(DEPARTMENTS_FILE)

    name_input = ask_valid("Department name to delete", is_not_empty,
                           "Name cannot be empty.")
    name = find_department(departments, clean_name(name_input))
    if name is None:
        print("Error: department not found.")
        return

    # A department that still has employees must not be deleted.
    employees = load_data(EMPLOYEES_FILE)
    count = 0
    for employee in employees:
        if employee["department"].lower() == name.lower():
            count += 1
    if count > 0:
        print(f"Cannot delete '{name}': {count} employee(s) are assigned to it.")
        return

    if ask_yes_no(f"Are you sure you want to delete '{name}'?"):
        departments.remove(name)
        save_data(DEPARTMENTS_FILE, departments)
        print("Department deleted.")
    else:
        print("Deletion cancelled.")


def department_menu():
    while True:
        print_heading("DEPARTMENT MANAGEMENT")
        print("1. Add Department")
        print("2. View All Departments")
        print("3. Search Department")
        print("4. Rename Department")
        print("5. Delete Department")
        print("6. Back to Main Menu")
        choice = input("\nEnter your choice: ").strip()

        if choice == "1":
            add_department()
        elif choice == "2":
            view_departments()
        elif choice == "3":
            search_department()
        elif choice == "4":
            rename_department()
        elif choice == "5":
            delete_department()
        elif choice == "6":
            break
        else:
            print("Invalid choice. Please enter a number from 1 to 6.")
