import os
import pathlib
import logging

logger = logging.getLogger(__name__)
logger.setLevel('DEBUG')


__CURRENT_DIRECTORY = pathlib.Path(__file__).parent.absolute()

PATH_TO_APP_LOGS = str(__CURRENT_DIRECTORY) + os.sep + ".." + os.sep + "logs" + os.sep + "app_logs.log"
PATH_TO_TEST_LOGS = str(__CURRENT_DIRECTORY) + os.sep + ".." + os.sep + "logs" + os.sep + "test_logs.log"
PATH_TO_DB = str(__CURRENT_DIRECTORY) + os.sep + ".." + os.sep + "db" + os.sep + "phone_book.sqlite"


def check_if_dir_exists():
    if not os.path.exists(str(__CURRENT_DIRECTORY) + os.sep + ".." + os.sep + "logs"):
        try:
            os.mkdir(str(__CURRENT_DIRECTORY) + os.sep + ".." + os.sep + "logs")
            logger.debug("Dir for logs has been created")
        except OSError:
            logger.debug(f"Creation of the directory {str(__CURRENT_DIRECTORY) + os.sep + '..' + os.sep + 'logs'} failed")

    if not os.path.exists(str(__CURRENT_DIRECTORY) + os.sep + ".." + os.sep + "db"):
        try:
            os.mkdir(str(__CURRENT_DIRECTORY) + os.sep + ".." + os.sep + "db")
            logger.debug("Dir for DB has been created")
        except OSError:
            logger.debug(f"Creation of the directory {str(__CURRENT_DIRECTORY) + os.sep + '..' + os.sep + 'db'} failed")


check_if_dir_exists()
