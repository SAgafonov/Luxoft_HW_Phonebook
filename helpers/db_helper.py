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
            return 0
        except sql.Error as e:
            logger.error(f"Error '{e}' on table creation")
            return 1

    def execute_query(self, query: str):
        """
        Execute not SELECT queries.
        :param query: str
        :return:
        """
        try:
            self.__cursor.execute(query)
            self.__connection.commit()
            return 0
        except sql.Error as e:
            logger.error(f"Error '{e}' while executing {query}")
            return 1

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


# dbi = MyDb()
# # dbi.create_table()
# ids = (1, 2)
# ins_q = "INSERT INTO phone_book (name, phone_number) VALUES ('test3', 434);"
# sel_q = "SELECT * FROM phone_book;"
# del_q = f"DELETE FROM phone_book;"
# # dbi.execute_query(ins_q)
# # dbi.execute_query(del_q)
# print(dbi.execute_read_query(sel_q))

# https://proglib.io/p/kak-podruzhit-python-i-bazy-dannyh-sql-podrobnoe-rukovodstvo-2020-02-27
