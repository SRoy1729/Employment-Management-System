"""
salary.py
Purpose: Simple salary management - view salaries, search by Employee ID,
update the basic salary and show the annual salary (monthly x 12).
There is no tax or payroll logic on purpose.
"""

from storage import EMPLOYEES_FILE, load_data, save_data
from helpers import (print_heading, print_line, format_money, ask_valid,
                     is_valid_salary)
from employee import ask_for_employee


def calculate_annual_salary(monthly_salary):
    """Annual Salary = Monthly Basic Salary x 12"""
    return monthly_salary * 12


def print_salary_info(employee):
    monthly = employee["basic_salary"]
    annual = calculate_annual_salary(monthly)
    print_line()
    print("Employee ID    :", employee["employee_id"])
    print("Name           :", employee["name"])
    print("Monthly Salary :", format_money(monthly))
    print("Annual Salary  :", format_money(annual))
    print_line()


def view_all_salaries():
    print_heading("ALL EMPLOYEE SALARIES")
    employees = load_data(EMPLOYEES_FILE)

    if len(employees) == 0:
        print("No employees are registered yet.")
        return

    print(f"{'ID':<8}{'Name':<22}{'Monthly':>18}{'Annual':>20}")
    print("-" * 68)
    for employee in employees:
        monthly = employee["basic_salary"]
        annual = calculate_annual_salary(monthly)
        print(f"{employee['employee_id']:<8}"
              f"{employee['name'][:20]:<22}"
              f"{format_money(monthly):>18}"
              f"{format_money(annual):>20}")


def view_salary_by_id():
    print_heading("SEARCH SALARY BY EMPLOYEE ID")
    employees = load_data(EMPLOYEES_FILE)
    employee = ask_for_employee(employees)
    if employee is not None:
        print_salary_info(employee)


def update_salary():
    print_heading("UPDATE BASIC SALARY")
    employees = load_data(EMPLOYEES_FILE)
    employee = ask_for_employee(employees)
    if employee is None:
        return

    print("\nCurrent salary:")
    print_salary_info(employee)

    new_salary = ask_valid("New monthly basic salary", is_valid_salary,
                           "Enter a number greater than 0 (no negatives).")
    employee["basic_salary"] = float(new_salary)

    if save_data(EMPLOYEES_FILE, employees):
        print("\nSalary updated successfully. New salary details:")
        print_salary_info(employee)


def salary_menu():
    while True:
        print_heading("SALARY MANAGEMENT")
        print("1. View All Employee Salaries")
        print("2. Search Salary by Employee ID")
        print("3. Update Basic Salary")
        print("4. Back to Main Menu")
        choice = input("\nEnter your choice: ").strip()

        if choice == "1":
            view_all_salaries()
        elif choice == "2":
            view_salary_by_id()
        elif choice == "3":
            update_salary()
        elif choice == "4":
            break
        else:
            print("Invalid choice. Please enter a number from 1 to 4.")
