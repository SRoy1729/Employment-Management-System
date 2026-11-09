"""
storage.py
Purpose: Handles ALL reading and writing of JSON files.
Other files never open JSON files directly; they call load_data() and save_data().
"""

import json
import os

# Find the folder where this file lives, so the program works
# no matter where you start it from.
BASE_FOLDER = os.path.dirname(os.path.abspath(__file__))
DATA_FOLDER = os.path.join(BASE_FOLDER, "data")

EMPLOYEES_FILE = os.path.join(DATA_FOLDER, "employees.json")
DEPARTMENTS_FILE = os.path.join(DATA_FOLDER, "departments.json")
ATTENDANCE_FILE = os.path.join(DATA_FOLDER, "attendance.json")

# These departments are added the very first time the program runs.
DEFAULT_DEPARTMENTS = [
    "Human Resources",
    "Finance",
    "Marketing",
    "IT",
    "Sales",
    "Operations",
]


def save_data(file_path, data):
    """Write a list to a JSON file (UTF-8). Replaces the old content."""
    try:
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
        return True
    except OSError as error:
        print("Error: could not save data ->", error)
        return False


def load_data(file_path):
    """
    Read a JSON file and return its list.
    - Missing file  -> returns an empty list.
    - Empty file    -> returns an empty list.
    - Broken JSON   -> the bad file is renamed to .bak (so nothing is lost)
                       and an empty list is returned.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            text = file.read()

        if text.strip() == "":
            return []

        data = json.loads(text)
        if not isinstance(data, list):
            raise ValueError("JSON file must contain a list")
        return data

    except FileNotFoundError:
        return []
    except ValueError:
        # json.JSONDecodeError is a kind of ValueError, so this catches both.
        print("Warning: the file", os.path.basename(file_path), "is damaged.")
        try:
            os.replace(file_path, file_path + ".bak")
            print("A backup copy was saved as", os.path.basename(file_path) + ".bak")
        except OSError:
            pass
        return []
    except OSError as error:
        print("Error: could not read file ->", error)
        return []


def create_file_if_missing(file_path, starting_data):
    """Create a JSON file with starting data, only if it does not exist yet."""
    if not os.path.exists(file_path):
        save_data(file_path, starting_data)


def setup_storage():
    """Create the data folder and the three JSON files when they are missing."""
    os.makedirs(DATA_FOLDER, exist_ok=True)
    create_file_if_missing(EMPLOYEES_FILE, [])
    create_file_if_missing(DEPARTMENTS_FILE, DEFAULT_DEPARTMENTS)
    create_file_if_missing(ATTENDANCE_FILE, [])
