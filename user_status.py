"""This module conatins the classes UserStatus and UserStatusCollection"""
# pylint: disable=R0903 (too-few-public-methods)
# pylint: disable=E0401 (import-error)
# pylint: disable=C0301 (line-too-long)
from loguru import logger


class UserStatus:
    """This class store information related to a user status update."""

    def __init__(self, status_id: str, user_id: str, status_text: str):
        """creates a UserStatus"""
        self.status_id = status_id
        self.user_id = user_id
        self.status_text = status_text
        logger.debug(f'Users({status_id}: str, {user_id}: str, {status_text}: str)')


class UserStatusCollection:
    """This class contains a database of UserStatus objects, and
    various functions to manipulate those UserStatus objects."""

    def __init__(self):
        self.database = {}
        logger.debug("UserStatusCollection()")

    def add_status(self, status_id: str, user_id: str, status_text: str):
        """This adds a status to the database."""
        if status_id in self.database:
            # Rejects new status if status_id already exists
            logger.warning(f'status_id:{status_id} in database, can not add')
            return False
        new_status = UserStatus(status_id, user_id, status_text)
        logger.debug(f"UserStatus({status_id}, {user_id}, {status_text})")
        self.database[status_id] = new_status
        return True

    def modify_status(self, status_id: str, user_id: str, status_text: str):
        """This changes the stored content in a status."""
        if status_id not in self.database:
            # Rejects update is the status_id does not exist
            logger.warning(f'status_id:{status_id} not in database, can not modify')
            return False
        self.database[status_id].user_id = user_id
        self.database[status_id].status_text = status_text
        logger.debug(f'new_user_id:{user_id}, new_status_text:{status_text}')
        return True

    def delete_status(self, status_id: str):
        """This deletes a status."""
        if status_id not in self.database:
            # Fails if status does not exist
            logger.warning(f'status_id:{status_id} not in database, can not delete')
            return False
        del self.database[status_id]
        logger.debug(f"del self.database[{status_id}]")
        return True

    def search_status(self, status_id: str):
        """This returns a status."""
        if status_id not in self.database:
            # Fails if the status does not exist
            logger.warning(f'status_id:{status_id} not in database, can not return')
            return UserStatus(None, None, None)
        logger.debug(f"return self.database[{status_id}]")
        return self.database[status_id]
