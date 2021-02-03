"""
Classes for user information for the
social network project
"""
# pylint: disable=R0903 (too-few-public-methods)
# pylint: disable=E0401 (import-error)
# pylint: disable=C0301 (line-too-long)

from loguru import logger


class Users:
    """
    Contains user information
    """

    def __init__(self, user_id: str, email: str, user_name: str, user_last_name: str):
        self.user_id = user_id
        self.email = email
        self.user_name = user_name
        self.user_last_name = user_last_name
        logger.debug(f'Users({user_id}: str, {email}: str, {user_name}: str, {user_last_name}: str)')


class UserCollection:
    """
    Contains a collection of Users objects
    """

    def __init__(self):
        self.database = {}
        logger.debug('UserCollection()')

    def add_user(self, user_id: str, email: str, user_name: str, user_last_name: str):
        """
        Adds a new user to the collection
        """
        if user_id in self.database:
            logger.warning(f'user_id:{user_id} in database, can not add')
            # Rejects new status if status_id already exists
            return False
        new_user = Users(user_id, email, user_name, user_last_name)
        logger.debug(f'Users({user_id}: str, {email}: str, {user_name}: str, {user_last_name}: str)')
        self.database[user_id] = new_user
        return True

    def modify_user(self, user_id: str, email: str, user_name: str, user_last_name: str):
        """
        Modifies an existing user
        """
        if user_id not in self.database:
            logger.warning(f'user_id:{user_id} not in database, can not modify')
            return False
        self.database[user_id].email = email
        self.database[user_id].user_name = user_name
        self.database[user_id].user_last_name = user_last_name
        logger.debug(f'new_email:{email}, new_user_name:{user_name}, new_user_last_name:{user_last_name}')
        return True

    def delete_user(self, user_id: str):
        """
        Deletes an existing user
        """
        if user_id not in self.database:
            logger.warning(f'user_id:{user_id} not in database, can not delete')
            return False
        del self.database[user_id]
        logger.debug(f"del self.database[{user_id}]")
        return True

    def search_user(self, user_id: str):
        """
        Searches for user data
        """
        if user_id not in self.database:
            logger.warning(f'user_id:{user_id} not in database, can not return')
            return Users(None, None, None, None)
        logger.debug(f"return self.database[{user_id}]")
        return self.database[user_id]
