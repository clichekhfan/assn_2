""" This module contains the main public functions for the program"""
# pylint: disable=R0903 (too-few-public-methods)
# pylint: disable=E0401 (import-error)
# pylint: disable=C0103 (invalid-name)
# pylint: disable=C0301 (line-too-long)
import csv
from menu import logger
import users
import user_status


def init_user_collection():
    """
    Creates and returns a new instance
    of UserCollection
    """
    collection = users.UserCollection()
    logger.debug('collection = users.UserCollection()')

    return collection


def init_status_collection():
    """
    Creates and returns a new instance
    of UserStatusCollection
    """
    stati = user_status.UserStatusCollection()
    logger.debug('stati = user_status.UserStatusCollection()')

    return stati


def load_users(filename, user_collection):
    """
    Opens a CSV file with user data and
    adds it to an existing instance of
    UserCollection

    Requirements:
    - If a user_id already exists, it
    will ignore it and continue to the
    next.
    - Returns False if there are any errors
    (such as empty fields in the source CSV file)
    - Otherwise, it returns True.
    """
    # read file
    accounts = []
    try:
        with open(filename, 'r', newline='') as csvfile:
            filereader = csv.reader(csvfile, delimiter=',', quotechar='|')
            for row in filereader:
                accounts.append(row)
        accounts = accounts[1:]
    except FileNotFoundError:
        logger.error('ERROR: FileNotFound')
        return False

    try:
        # pass data to user collection
        ref_list = []  # ref_list will be a list of user_ids
        for user_id in user_collection.database:
            ref_list.append(user_id)

        # check for existing users
        new_accounts = []
        for row in accounts:
            if row[0] not in ref_list:
                new_accounts.append(row)
        # pass new accounts to user collection
        for account in new_accounts:
            user_collection.add_user(*account)
    except TypeError as e:
        logger.error('ERROR: Could not load users!')
        logger.info(f'load_users({filename}, {user_collection})')
        logger.debug(f'{e}')
        try:
            logger.debug(f'{user_collection}.add_user(*{account})')
        except UnboundLocalError:
            logger.error(f'ERROR: {user_collection}.add_user(*account), UnboundLocalError')
        return False

    return True


def save_users(filename, user_collection):
    """
    Saves all users in user_collection into
    a CSV file

    Requirements:
    - If there is an existing file, it will
    overwrite it.
    - Returns False if there are any errors
    (such an invalid filename).
    - Otherwise, it returns True.
    """
    # create CSV strings
    lines = ['USER_ID,EMAIL,NAME,LASTNAME']
    for user_id, user_obj in user_collection.database.items():
        email = user_obj.email
        user_name = user_obj.user_name
        user_last_name = user_obj.user_last_name

        line = f'{user_id},{email},{user_name},{user_last_name}'
        lines.append(line)
    text = '\n'.join(lines)

    try:
        with open(filename, 'w') as csvfile:
            csvfile.write(text)
    except OSError:
        return False

    return True


def load_status_updates(filename, status_collection):
    """
    Opens a CSV file with status data and
    adds it to an existing instance of
    UserStatusCollection

    Requirements:
    - If a status_id already exists, it
    will ignore it and continue to the
    next.
    - Returns False if there are any errors
    (such as empty fields in the source CSV file)
    - Otherwise, it returns True.
    """

    # read file
    stati = []
    try:
        with open(filename, newline='') as csvfile:
            filereader = csv.reader(csvfile, delimiter=',', quotechar='|')
            for row in filereader:
                stati.append(row)
        stati = stati[1:]  # delete header
    except FileNotFoundError:
        logger.error('ERROR: FileNotFound')
        return False

    try:
        # pass data to user collection
        ref_list = []  # ref_list will be a list of user_ids
        for status_id in status_collection.database:
            ref_list.append(status_id)
        print(ref_list)

        # check for existing users
        new_stati = []
        for row in stati:
            if row[0] not in ref_list:
                new_stati.append(row)
        print(new_stati)

        # pass new accounts to user collection
        for status_details in new_stati:
            status_collection.add_status(*status_details)
    except TypeError:
        logger.error('ERROR: TypeError')
        return False
    except IndexError:
        logger.error('ERROR: IndexError')
        return False

    return True


def save_status_updates(filename, status_collection):
    """
    Saves all statuses in status_collection into
    a CSV file

    Requirements:
    - If there is an existing file, it will
    overwrite it.
    - Returns False if there are any errors
    (such an invalid filename).
    - Otherwise, it returns True.
    """
    # create CSV strings
    lines = ['STATUS_ID,USER_ID,STATUS_TEXT']
    for status_id, status_obj in status_collection.database.items():
        user_id = status_obj.user_id
        status_text = status_obj.status_text

        line = f'{status_id},{user_id},{status_text}'
        lines.append(line)
    text = '\n'.join(lines)

    try:
        with open(filename, 'w') as csvfile:
            csvfile.write(text)
    except OSError:
        return False

    return True


def add_user(user_id, email, user_name, user_last_name, user_collection):
    """
    Creates a new instance of User and stores it in user_collection
    (which is an instance of UserCollection)

    Requirements:
    - user_id cannot already exist in user_collection.
    - Returns False if there are any errors (for example, if
    user_collection.add_user() returns False).
    - Otherwise, it returns True.
    """
    for database_user_id, _ in user_collection.database.items():
        if database_user_id == user_id:
            return False

    user_collection.add_user(user_id, email, user_name, user_last_name)
    return True


def update_user(user_id, email, user_name, user_last_name, user_collection):
    """
    Updates the values of an existing user

    Requirements:
    - Returns False if there any errors.
    - Otherwise, it returns True.
    """
    params = (user_id, email, user_name, user_last_name)
    result = user_collection.modify_user(*params)

    return result


def delete_user(user_id, user_collection):
    """
    Deletes a user from user_collection.

    Requirements:
    - Returns False if there are any errors (such as user_id not found)
    - Otherwise, it returns True.
    """
    result = user_collection.delete_user(user_id)

    return result


def search_user(user_id, user_collection):
    """
    Searches for a user in user_collection
    (which is an instance of UserCollection).

    Requirements:
    - If the user is found, returns the corresponding
    User instance.
    - Otherwise, it returns None.
    """
    result = user_collection.search_user(user_id)

    if result.user_id is None:
        return None

    return result


def add_status(user_id, status_id, status_text, status_collection):
    """
    Creates a new instance of UserStatus and stores it in user_collection
    (which is an instance of UserStatusCollection)

    Requirements:
    - status_id cannot already exist in user_collection.
    - Returns False if there are any errors (for example, if
    user_collection.add_status() returns False).
    - Otherwise, it returns True.
    """
    result = status_collection.add_status(status_id, user_id, status_text)

    return result


def update_status(status_id, user_id, status_text, status_collection):
    """
    Updates the values of an existing status_id

    Requirements:
    - Returns False if there any errors.
    - Otherwise, it returns True.
    """
    result = status_collection.modify_status(status_id, user_id, status_text)

    return result


def delete_status(status_id, status_collection):
    """
    Deletes a status_id from user_collection.

    Requirements:
    - Returns False if there are any errors (such as status_id not found)
    - Otherwise, it returns True.
    """
    result = status_collection.delete_status(status_id)

    return result


def search_status(status_id, status_collection):
    """
    Searches for a status in status_collection

    Requirements:
    - If the status is found, returns the corresponding
    UserStatus instance.
    - Otherwise, it returns None.
    """
    result = status_collection.search_status(status_id)

    if result.status_id is None:
        return None

    return result
