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
                              ("q"*20, True),
                              ("", False),
                              ("  ", False),
                              ("z"*21, False)])
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
                             [("to_be_deleted", 54676, "Data saved"),
                              ("'", 1200, None),
                              ("John", 54676, "Phone 54676 already exists")])
    def test_save_contact(self, phone_book, name, phone, expected, del_contacts):
        logger.debug(f"Run test_save_contact: name '{name}', phone '{phone}'")
        assert phone_book.save_contact(name, phone) == expected

    @pytest.mark.parametrize("name, expected",
                             [("John", ("John", 123)),
                              ("Петр Иванов", ("Петр Иванов", 5434563)),
                              ("Jo", ("John", 123))])
    def test_find_contact(self, phone_book, name, expected, del_contacts, create_contacts):
        logger.debug(f"Run test_find_contact: name '{name}', expected result '{expected}'")
        for contact in phone_book.find_contact(name):
            assert contact[1:] == expected

    @pytest.mark.parametrize("expected",
                             [[("John", 123), ("Петр Иванов", 5434563)]])
    def test_get_all_contacts(self, phone_book, expected, del_contacts_function_scope, create_contacts_function_scope):
        logger.debug(f"Run test_get_all_contacts: expected result '{expected}'")
        result = []
        for contact in phone_book.get_all_contacts():
            result.append(contact[1:])
        assert result == expected

    @pytest.mark.parametrize("name", ["John"])
    def test_delete_contact(self, phone_book, name, del_contacts, create_contacts):
        logger.debug(f"Run test_delete_contact:  name '{name}'")
        contact_id = phone_book.find_contact(name)[0][0]
        assert phone_book.delete_contact(contact_id) == "Contact was deleted"
        assert not phone_book.find_contact(name)

    def test_delete_contacts(self, phone_book, create_contacts_function_scope):
        logger.debug(f"Run test_delete_contacts")
        contacts_ids = []
        for contact in phone_book.get_all_contacts():
            contacts_ids.append(contact[0])
        assert phone_book.delete_contacts(tuple(contacts_ids)) == "Contacts were deleted"
        assert not phone_book.get_all_contacts()
