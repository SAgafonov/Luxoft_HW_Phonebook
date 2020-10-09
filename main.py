import logging
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from helpers.phone_book import PhoneBook
from helpers.configuration import PATH_TO_APP_LOGS

# Configure general settings for logs
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s:%(levelname)s:%(filename)s:%(funcName)s() - %(message)s',
    filemode='w',   # Rewrite logs
    filename=PATH_TO_APP_LOGS
)
logger = logging.getLogger(__name__)


pb = PhoneBook()
window = tk.Tk()

# Store all check-boxes on contacts_frame
check_box_list = []
# Store correspondence of check-box to a contact
id_to_check_box = {}


def add_contact():
    """
    Function for Add button.
    Check if provided name is correct, strip leading and trailing spaces, replace ' with ''
    :return:
    """
    contact_name = add_name_entry.get()
    contact_phone = add_phone_entry.get()
    logger.debug(f"Check if name {contact_name} and phone {contact_phone} correct")
    if not pb.name_is_correct(contact_name.strip(" ")):
        logger.debug("Name is incorrect")
        messagebox.showwarning("Warning", "Check 'Name' it shouldn't be empty, max length is 255 chars")
    elif not pb.phone_is_correct(contact_phone.strip(" ")):
        logger.debug("Phone is incorrect")
        messagebox.showwarning("Warning", "Check 'Phone' it shouldn't be empty and must include numbers only, "
                                          "max length is 20 numbers")
    else:
        logger.debug("Name and phone are correct. Save data.")
        result = pb.save_contact(contact_name.strip(" ").replace("'", "''"), int(contact_phone))
        messagebox.showinfo("Info", result)
        add_name_entry.delete(0, tk.END)
        add_phone_entry.delete(0, tk.END)


def find_contact():
    """
    Function for Find button.
    Check if provided name is correct, strip leading and trailing spaces, replace ' with ''.
    Check if contact exists.
    Call function to show checkboxes with contacts
    :return:
    """
    contact_name_to_find = find_name_entry.get()
    logger.debug(f"Check if name {contact_name_to_find} is correct")
    if not pb.name_is_correct(contact_name_to_find.strip(" ")):
        logger.debug("Name is incorrect")
        messagebox.showwarning("Warning", "Check 'Name' it shouldn't be empty, max length is 255 chars")
    else:
        logger.debug("Name is correct. Find contact.")
        result = pb.find_contact(contact_name_to_find.strip(" ").replace("'", "''"))
        if len(result):
            represent_checkboxes(result)
        # for item in result:
        #     chk_box = ttk.Checkbutton(contacts_frame, text=f"Name: {item[1]}, Phone: {item[2]}")
        #     chk_box.grid()
        #     check_box_list.append(chk_box)
        #     id_to_check_box[item[0]] = chk_box
            find_name_entry.delete(0, tk.END)
        else:
            logger.debug(f"Contact {contact_name_to_find} not found")
            messagebox.showinfo("Info", f"Contact with name '{contact_name_to_find}' not found")


def clear_chk_boxes():
    """
    Function to remove all check-boxes in 'Contacts' frame
    :return:
    """
    logger.debug("Remove all check-boxes")
    for check_box in check_box_list:
        check_box.destroy()


def delete_contacts():
    """
    Function for Delete button.
    Remove contacts that were chosen.
    :return:
    """
    contacts_to_remove = []
    logger.debug("Choose what contacts to delete")
    for idx in id_to_check_box:
        if 'selected' in id_to_check_box[idx].state():
            contacts_to_remove.append(idx)
    if not len(contacts_to_remove):
        messagebox.showwarning("Warning", "You should check at least one contact.")
    elif len(contacts_to_remove) == 1:
        logger.debug("Delete a contact")
        result = pb.delete_contact(contacts_to_remove[0])
        if result:
            messagebox.showinfo("Info", result)
            show_all_contacts()
        else:
            messagebox.showwarning("Warning", "Can't execute request. Try restart program.")
    else:
        logger.debug("Delete contactS")
        result = pb.delete_contacts(tuple(map(int, contacts_to_remove)))
        if result:
            messagebox.showinfo("Info", result)
            show_all_contacts()
        else:
            messagebox.showwarning("Warning", "Can't execute request. Try restart program.")


def show_all_contacts():
    """
    Function for Show all button.
    Represent all saved contacts.
    :return:
    """
    result = pb.get_all_contacts()
    logger.debug("Show all contacts")
    represent_checkboxes(result)
    find_name_entry.delete(0, tk.END)


def represent_checkboxes(contacts: list):
    """
    Shows list of contacts with check-boxes.
    :param contacts: list
    :return:
    """
    clear_chk_boxes()
    id_to_check_box.clear()
    logger.debug("Show check-boxes")
    for item in contacts:
        chk_box = ttk.Checkbutton(contacts_frame, text=f"Name: {item[1]},\nPhone: {item[2]}")
        chk_box.grid(sticky=tk.W)
        check_box_list.append(chk_box)
        id_to_check_box[item[0]] = chk_box


# Tabs on main window
window.title("Phone book")
window.iconbitmap("icons/icon.ico")
window.geometry("300x300+700+300")
tab_control = ttk.Notebook(window)
tab_add_contact = ttk.Frame(tab_control)
tab_find_contact = ttk.Frame(tab_control)
tab_control.add(tab_add_contact, text='Add contact')
tab_control.add(tab_find_contact, text='Find contact')

window.columnconfigure(1, weight=0, minsize=20)
window.rowconfigure(0, weight=0, minsize=20)

# Widgets on Add form
add_button = tk.Button(tab_add_contact, text='Add', width=15, command=add_contact)
add_name_entry = tk.Entry(tab_add_contact)
add_phone_entry = tk.Entry(tab_add_contact)
add_name_label = tk.Label(tab_add_contact, text="Name")
add_phone_label = tk.Label(tab_add_contact, text="Phone")
add_name_label.grid(column=0, row=0, padx=10, pady=5, sticky=tk.S)
add_name_entry.grid(column=0, row=1, padx=10, sticky=tk.E)
add_phone_label.grid(column=1, row=0, padx=10, pady=5, sticky=tk.S)
add_phone_entry.grid(column=1, row=1, padx=10, sticky=tk.E)
add_button.grid(column=0, row=3, padx=10, pady=10, sticky=tk.S, columnspan=2)

# Widgets on Find form
find_button = tk.Button(tab_find_contact, text='Find', width=15, height=3, bg="green", command=find_contact)
delete_button = tk.Button(tab_find_contact, text='Delete', width=15, height=3, bg="red", command=delete_contacts)
show_all_button = tk.Button(tab_find_contact, text='Show all', width=15, height=3, bg="yellow", command=show_all_contacts)
find_name_entry = tk.Entry(tab_find_contact)
find_name_label = tk.Label(tab_find_contact, text="Name")
contacts_frame = tk.LabelFrame(tab_find_contact, text="Contacts", padx=5, pady=5, width=5)
contacts_frame.grid(column=0, row=2, padx=10, pady=5, rowspan=25)
find_name_label.grid(column=0, row=0, padx=5, pady=5, sticky=tk.S)
find_name_entry.grid(column=0, row=1, padx=10, sticky=tk.W)
find_button.grid(column=1, row=0, padx=10, rowspan=2)
delete_button.grid(column=1, row=2, padx=10, rowspan=2)
show_all_button.grid(column=1, row=4, padx=10, rowspan=2)

# Run
tab_control.pack(expand=1, fill='both')
window.mainloop()


# https://coderoad.ru/17466561/%D0%9B%D1%83%D1%87%D1%88%D0%B8%D0%B9-%D1%81%D0%BF%D0%BE%D1%81%D0%BE%D0%B1-%D1%81%D1%82%D1%80%D1%83%D0%BA%D1%82%D1%83%D1%80%D0%B8%D1%80%D0%BE%D0%B2%D0%B0%D1%82%D1%8C-%D0%BF%D1%80%D0%B8%D0%BB%D0%BE%D0%B6%D0%B5%D0%BD%D0%B8%D0%B5-tkinter
# https://pythonru.com/uroki/obuchenie-python-gui-uroki-po-tkinter
# https://ru.stackoverflow.com/questions/885677/%D0%92%D1%82%D0%BE%D1%80%D0%BE%D0%B5-%D0%BE%D0%BA%D0%BD%D0%BE-tkinter
