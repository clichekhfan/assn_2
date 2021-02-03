"""
Provides a basic frontend
"""
# pylint: disable=R0903 (too-few-public-methods)
# pylint: disable=E0401 (import-error)
# pylint: disable=C0301 (line-too-long)
# pylint: disable=W0601 (global-variable-undefined)
# pylint: disable=C0103 (invalid-name)
# pylint: disable=C0116 (missing-function-docstring)

import sys
import os
import datetime
from loguru import logger
import main

date = datetime.date.today()

try:
    if not os.path.exists('logs'):
        os.makedirs('logs')

    path = os.path.join('logs', f'log__{date}.log')

    with open(path, 'w'):
        pass
except Exception as e:
    logger.warning('ERROR:', e)
    raise e

logger.add(path)  # took me a while to figure out the best format="" is format=default
# format="{time} {level} {message}" does not include the module:func:line


def load_users():
    """
    Loads user accounts from a file
    """

    filename = input('Enter filename of user file: ')
    if not main.load_users(filename, user_collection):
        print("An error occurred while trying to load users")
    else:
        print("Load users was successful")


def load_status_updates():
    """
    Loads status updates from a file
    """
    filename = input('Enter filename for status file: ')
    if not main.load_status_updates(filename, status_collection):
        print("An error occurred while trying to load status updates")
    else:
        print("Load status updates was successful")


def add_user():
    """
    Adds a new user into the database
    """
    user_id = input('User ID: ')
    email = input('User email: ')
    user_name = input('User name: ')
    user_last_name = input('User last name: ')
    if not main.add_user(user_id, email, user_name, user_last_name, user_collection):
        print("An error occurred while trying to add new user")
    else:
        print("User was successfully added")


def update_user():
    """
    Updates information for an existing user
    """
    user_id = input('User ID: ')
    email = input('User email: ')
    user_name = input('User name: ')
    user_last_name = input('User last name: ')
    if not main.update_user(user_id, email, user_name, user_last_name, user_collection):
        print("An error occurred while trying to update user")
    else:
        print("User was successfully updated")


def search_user():
    """
    Searches a user in the database
    """
    user_id = input('Enter user ID to search: ')
    result = main.search_user(user_id, user_collection)
    if result is None:
        print("ERROR: User does not exist")
    else:
        print(f"User ID: {result.user_id}")
        print(f"Email: {result.email}")
        print(f"Name: {result.user_name}")
        print(f"Last name: {result.user_last_name}")


def delete_user():
    """
    Deletes user from the database
    """
    user_id = input('User ID: ')
    if not main.delete_user(user_id, user_collection):
        print("An error occurred while trying to delete user")
    else:
        print("User was successfully deleted")


def save_users():
    """
    Saves user database into a file
    """
    filename = input('Enter filename for users file: ')
    main.save_users(filename, user_collection)
    if not main.save_users(filename, user_collection):
        print("An error occurred while trying to save users")
    else:
        print("save users was successful")


def add_status():
    """
    Adds a new status into the database
    """
    status_id = input('Status ID: ')
    user_id = input('User ID: ')
    status_text = input('Status text: ')
    if not main.add_status(user_id, status_id, status_text, status_collection):
        print("An error occurred while trying to add new status")
    else:
        print("New status was successfully added")


def update_status():
    """
    Updates information for an existing status
    """
    status_id = input('Status ID: ')
    user_id = input('User ID: ')
    status_text = input('Status text: ')
    if not main.update_status(status_id, user_id, status_text, status_collection):
        print("An error occurred while trying to update status")
    else:
        print("Status was successfully updated")


def search_status():
    """
    Searches a status in the database
    """
    status_id = input('Enter status ID to search: ')
    result = main.search_status(status_id, status_collection)
    if result is None:
        print("ERROR: Status does not exist")
    else:
        print(f"User ID: {result.user_id}")
        print(f"Status ID: {result.status_id}")
        print(f"Status text: {result.status_text}")


def delete_status():
    """
    Deletes status from the database
    """
    status_id = input('Status ID: ')
    if not main.delete_status(status_id, status_collection):
        print("An error occurred while trying to delete status")
    else:
        print("Status was successfully deleted")


def save_status():
    """
    Saves status database into a file
    """
    filename = input('Enter filename for status file: ')
    if not main.save_status_updates(filename, status_collection):
        print("An error occurred while trying to save status updates")
    else:
        print("save status updates was successful")


def quit_program():
    """
    Quits program
    """
    print('Goodbye!')
    sys.exit()


def menu():
    global user_collection
    user_collection = main.init_user_collection()
    global status_collection
    status_collection = main.init_status_collection()
    menu_options = {
        'A': load_users,
        'B': load_status_updates,
        'C': add_user,
        'D': update_user,
        'E': search_user,
        'F': delete_user,
        'G': save_users,
        'H': add_status,
        'I': update_status,
        'J': search_status,
        'K': delete_status,
        'L': save_status,
        'Q': quit_program
    }
    while True:
        user_selection = input("""
    A: Load user database
    B: Load status database
    C: Add user
    D: Update user
    E: Search user
    F: Delete user
    G: Save user database to file
    H: Add status
    I: Update status
    J: Search status
    K: Delete status
    L: Save status database to file
    Q: Quit

    Please enter your choice: """)
        if user_selection.upper() in menu_options:
            menu_options[user_selection.upper()]()
        else:
            print("Invalid option")


if __name__ == '__main__':
    logger.debug(f'__name__:{__name__}')
    menu()
