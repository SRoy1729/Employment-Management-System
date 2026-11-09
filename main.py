"""
main.py
Purpose: The starting point of the program. It shows the main menu and
calls the right function for each choice. Run this file to start the system:
    python main.py
"""

from storage import setup_storage
from helpers import print_heading
from employee import (add_employee, view_employees, update_employee,
                      delete_employee, search_employee)
from salary import salary_menu
from department import department_menu
from attendance import attendance_menu


def show_main_menu():
    print_heading("EMPLOYMENT MANAGEMENT SYSTEM")
    print("1. Add Employee")
    print("2. View Employee Records")
    print("3. Update Employee Details")
    print("4. Delete Employee")
    print("5. Search Employee")
    print("6. Salary Management")
    print("7. Department Management")
    print("8. Attendance Management")
    print("9. Exit")
    print("=" * 60)


def main():
    setup_storage()   # creates the data folder and JSON files if missing

    try:
        while True:
            show_main_menu()
            choice = input("Enter your choice: ").strip()

            if choice == "1":
                add_employee()
            elif choice == "2":
                view_employees()
            elif choice == "3":
                update_employee()
            elif choice == "4":
                delete_employee()
            elif choice == "5":
                search_employee()
            elif choice == "6":
                salary_menu()
            elif choice == "7":
                department_menu()
            elif choice == "8":
                attendance_menu()
            elif choice == "9":
                print("\nAll data is saved. Thank you for using the system. Goodbye!")
                break
            else:
                print("Invalid choice. Please enter a number from 1 to 9.")
    except (KeyboardInterrupt, EOFError):
        # Ctrl+C pressed. Data is saved after every operation, so nothing is lost.
        print("\n\nProgram stopped. All saved data is safe. Goodbye!")


if __name__ == "__main__":
    main()
