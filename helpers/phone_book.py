import logging
from typing import Tuple, Union, List
from helpers.db_helper import MyDb

logger = logging.getLogger(__name__)
logger.setLevel('DEBUG')


class PhoneBook:
    def __init__(self):
        self.__db = MyDb()

    @staticmethod
    def name_is_correct(name: str) -> bool:
        """
        Check if len of provided name is in range (0, 20].
        :param name: str
        :return: bool
        """
        logger.debug("Check if name is correct")
        return 0 < len(name) < 21

    @staticmethod
    def phone_is_correct(phone: str) -> bool:
        """
        Check if len of provided phone is in range (0, 20] and only numbers were provided.
        :param phone: str
        :return: bool
        """
        logger.debug("Check if phone is correct")
        return 0 < len(phone) < 21 and phone.isdigit()

    def phone_exists(self, phone: int) -> bool:
        """
        Check if provided phone is already exists in DB.
        :param phone: str
        :return: bool
        """
        query = f"""SELECT id FROM phone_book WHERE phone_number = {phone};"""
        logger.debug(f"Check if phone {phone} already exists")
        return bool(self.__db.execute_read_query(query))

    def save_contact(self, name: str, phone: int) -> Union[str, None]:
        """
        Execute saving a contact.
        Return result of operation, None if INSERT was not successful.
        :param name: str
        :param phone: int
        :return: Union[str, None]
        """
        query = f"""
        INSERT INTO phone_book (name, phone_number) 
        VALUES ('{name}', '{phone}');
        """
        if not self.phone_exists(phone):
            logger.debug(f"Try to save contact {name}, {phone}")
            if self.__db.execute_query(query):
                logger.debug(f"Contact {name}, {phone} saved")
                return "Data saved"
            else:
                return None
        else:
            logger.debug(f"Contact with {phone} already exists")
            return f"Phone {str(phone)} already exists"

    def find_contact(self, name: str) -> List[Tuple[Union[int, str]]]:
        """
        Search for a provided contact.
        :param name: str
        :return: List[Tuple[Union[int, str]]]
        """
        query = f"""SELECT * FROM phone_book WHERE name LIKE '%{name}%';"""
        logger.debug(f"Search {name}")
        return self.__db.execute_read_query(query)

    def get_all_contacts(self) -> list:
        """
        Return all contacts, saved in DB
        :return: list
        """
        query = f"""SELECT * FROM phone_book;"""
        logger.debug("Return all contacts")
        return self.__db.execute_read_query(query)

    def delete_contact(self, idx: int) -> Union[str, None]:
        """
        Delete one provided contact.
        Id of contact is expected.
        Return result of operation, None if DELETE was not successful
        :param idx: int
        :return: Union[str, None]
        """
        query = f"""DELETE FROM phone_book WHERE id = {idx}"""
        logger.debug(f"Delete contact with id: {idx}")
        if self.__db.execute_query(query):
            return "Contact was deleted"
        else:
            return None

    def delete_contacts(self, ids: Tuple[int]) -> Union[str, None]:
        """
        Delete all provided contact.
        Tuple of Ids of contacts is expected.
        Return result of operation, None if DELETE was not successful
        :param ids: Tuple[int]
        :return: Union[str, None]
        """
        query = f"""DELETE FROM phone_book WHERE id IN {ids}"""
        logger.debug(f"Delete contacts with ids: {ids}")
        if self.__db.execute_query(query):
            return "Contacts were deleted"
        else:
            return None
