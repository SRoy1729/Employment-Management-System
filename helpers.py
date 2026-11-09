"""
helpers.py
Purpose: Small tools used by many files: asking the user for input safely,
checking (validating) that input, printing headings and formatting money.
Keeping them here means we write each of them only once.
"""

from datetime import datetime, date

CURRENCY = "Rs."          # Change this if you want another currency symbol.
DATE_FORMAT = "%Y-%m-%d"  # Dates look like 2025-01-31


# ---------------------------------------------------------------
# Printing helpers
# ---------------------------------------------------------------
def print_heading(title):
    """Print a title between two lines."""
    print()
    print("=" * 60)
    print(title.center(60))
    print("=" * 60)


def print_line():
    print("-" * 60)


def format_money(amount):
    """Turn 50000 into 'Rs. 50,000.00'."""
    return f"{CURRENCY} {amount:,.2f}"


def today_string():
    """Today's date as text, e.g. '2025-01-31'."""
    return date.today().strftime(DATE_FORMAT)


# ---------------------------------------------------------------
# Validation (check) functions. Each returns True if the text is OK.
# ---------------------------------------------------------------
def is_not_empty(text):
    return text.strip() != ""


def is_valid_age(text):
    if not text.isdecimal():
        return False
    age = int(text)
    return 18 <= age <= 70


def is_valid_gender(text):
    return text.strip().lower() in ["male", "female", "other"]


def is_valid_phone(text):
    # Only digits, between 10 and 15 of them.
    return text.isdecimal() and 10 <= len(text) <= 15


def is_valid_email(text):
    if " " in text or text.count("@") != 1:
        return False
    name_part, domain_part = text.split("@")
    if name_part == "" or "." not in domain_part:
        return False
    if domain_part.startswith(".") or domain_part.endswith("."):
        return False
    return True


def is_valid_date(text):
    """True for real dates written as YYYY-MM-DD, e.g. 2025-02-28."""
    if len(text) != 10:
        return False
    try:
        datetime.strptime(text, DATE_FORMAT)
        return True
    except ValueError:
        return False


def is_valid_joining_date(text):
    """A valid date that is not in the future."""
    if not is_valid_date(text):
        return False
    joining = datetime.strptime(text, DATE_FORMAT).date()
    return joining <= date.today()


def is_valid_salary(text):
    """A number greater than zero (negative or zero is not allowed)."""
    try:
        value = float(text)
    except ValueError:
        return False
    return 0 < value < 1000000000


# ---------------------------------------------------------------
# Input helpers
# ---------------------------------------------------------------
def ask_valid(prompt, check_function, error_message, current_value=None):
    """
    Keep asking until the user types something that passes check_function.

    If current_value is given (used when UPDATING), the user can just press
    Enter to keep the old value.
    """
    while True:
        if current_value is not None:
            text = input(f"{prompt} [{current_value}] (Enter to keep): ").strip()
            if text == "":
                return current_value
        else:
            text = input(f"{prompt}: ").strip()

        if check_function(text):
            return text
        print("Error:", error_message)


def ask_yes_no(question):
    """Ask a yes/no question. Returns True for yes, False for no."""
    while True:
        answer = input(f"{question} (y/n): ").strip().lower()
        if answer in ["y", "yes"]:
            return True
        if answer in ["n", "no"]:
            return False
        print("Please type y or n.")
