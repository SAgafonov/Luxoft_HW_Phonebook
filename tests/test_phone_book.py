import pytest
import logging

logger = logging.getLogger(__name__)
logger.setLevel('DEBUG')


class TestPhoneBook:

    @pytest.mark.parametrize("name, expected",
                             [("test", True),
                              (" test ", True),
                              ("Test test", True),
                              ("Иван Иванович Иванов", True),
                              ("J0hn", True),
                              ("!@#$$%&'`", True),
                              ("q"*255, True),
                              ("", False),
                              ("  ", False),
                              ("z"*256, False)])
    def test_name_correctness(self, phone_book, name, expected):
        logger.debug(f"Run test_name_correctness: '{name}' is correct {expected}")
        assert phone_book.name_is_correct(name.strip()) is expected

    @pytest.mark.parametrize("phone, expected",
                             [("1", True),
                              (" 123 ", True),
                              ("123", True),
                              ("12345678901234567890", True),
                              ("0", True),
                              ("-1", False),
                              ("0.99", False),
                              ("J0hn", False),
                              ("!@#$$%&'`", False),
                              ("цйук", False),
                              ("", False),
                              ("  ", False),
                              ("123456789012345678901", False)])
    def test_phone_correctness(self, phone_book, phone, expected):
        logger.debug(f"Run test_phone_correctness: phone '{phone}' is correct {expected}")
        assert phone_book.phone_is_correct(phone.strip()) is expected

    @pytest.mark.parametrize("phone, expected",
                             [(5667433, False),
                              (123, True)])
    def test_phone_exists(self, phone_book, phone, expected, del_contacts, create_contacts):
        logger.debug(f"Run test_phone_exists: phone '{phone}'")
        assert phone_book.phone_exists(phone) is expected

    @pytest.mark.parametrize("name, phone, expected",
                             [("Test", 54676, "Data saved"),
                              ("'", 1200, None),
                              ("John", 54676, "Phone 54676 already exists")])
    def test_save_contact(self, phone_book, name, phone, expected, del_contacts):
        logger.debug(f"Run test_save_contact: name '{name}', phone '{phone}'")
        assert phone_book.save_contact(name, phone) == expected
