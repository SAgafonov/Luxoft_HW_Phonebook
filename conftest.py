import pytest
import logging
from helpers.phone_book import PhoneBook
from helpers.configuration import PATH_TO_TEST_LOGS
from helpers.db_helper import MyDb

# Configure general settings for logs
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s:%(levelname)s:%(filename)s:%(funcName)s() - %(message)s',
    filemode='w',  # Rewrite logs
    filename=PATH_TO_TEST_LOGS
)
logger = logging.getLogger(__name__)


@pytest.fixture(scope="module")
def my_db():
    return MyDb()


@pytest.fixture(scope="module")
def phone_book():
    return PhoneBook()


@pytest.fixture(scope="class")
def create_contacts(my_db):
    logger.debug("Execute INSERT from fixture")
    query = """
            INSERT INTO phone_book (name, phone_number) 
            VALUES ('John', 123);
            """
    my_db.execute_query(query)


@pytest.fixture(scope="class")
def del_contacts(my_db):
    logger.debug("Execute DELETE from fixture")
    query = f"""DELETE FROM phone_book;"""
    my_db.execute_query(query)
