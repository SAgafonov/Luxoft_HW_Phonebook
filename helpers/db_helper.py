import logging
import sqlite3 as sql
from helpers.configuration import PATH_TO_DB

logger = logging.getLogger(__name__)
logger.setLevel('ERROR')


class MyDb:
    def __init__(self):
        self.__path_to_db = PATH_TO_DB
        self.__connection = self.__create_connection()
        self.__cursor = self.__connection.cursor()
        self.__create_table()

    def __del__(self):
        self.__cursor.close()
        self.__connection.close()

    def __create_connection(self) -> sql.Connection:
        """
        Return connection to DB.
        :return: Connection
        """
        try:
            return sql.connect(self.__path_to_db)
        except sql.Error as e:
            logger.error(f"Connection error '{e}'")

    def __create_table(self):
        """
        Create table.
        :return:
        """
        try:
            self.__cursor.execute("""CREATE TABLE IF NOT EXISTS phone_book (
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            name VARCHAR(255) NOT NULL, 
            phone_number INTEGER NOT NULL);
            """)
            self.__connection.commit()
            return 1
        except sql.Error as e:
            logger.error(f"Error '{e}' on table creation")
            return 0

    def execute_query(self, query: str):
        """
        Execute not SELECT queries.
        :param query: str
        :return:
        """
        try:
            self.__cursor.execute(query)
            self.__connection.commit()
            return 1
        except sql.Error as e:
            logger.error(f"Error '{e}' while executing {query}")
            return 0

    def execute_read_query(self, query: str) -> list:
        """
        Execute SELECT queries and return result.
        :param query: str
        :return: list
        """
        try:
            self.__cursor.execute(query)
            result = self.__cursor.fetchall()
            return result
        except sql.Error as e:
            logger.error(f"Error '{e}' while executing {query}")
