# Luxoft HW - Phonebook
Application 'Phonebook' can be used to store contacts. 
When you run the application you will see two tabs: one for adding contacts and another
one for searching, deleting and getting all contacts.
#### Add contact tab
**Name** field - any string, including symbols. May contain spaces. Max length 20 chars.  
**Phone** field - digits only. Any other symbol is forbidden.  Max length 20 chars.
#### Find contact tab
**Name** field - any string, including symbols. May contain spaces. Max length 20 chars.  
To delete contact(-s) you need to find at least one, check appropriate check-box and push "Delete" button.
### Getting started
Make sure the you have installed Python 3.8 or higher.  
Clone the project.  
Install requirements:  
`pip install -r requirements.txt` 
To run application execute  
`python <path_to_project_root_folder>\main.py` -- Windows  
`python3 <path_to_project_root_folder>/main.py` -- Linux
### Running tests
Use folder `tests` 
Tests without a report:  
`pytest <path_to_project_tests_folder>\test_phone_book.py` -- Windows  
`pytest <path_to_project_tests_folder>/test_phone_book.py` -- Linux  
Tests with a report - report.html will be generated in a current directory:  
`pytest --html=report.html <path_to_project_tests_folder>\test_phone_book.py` -- Windows   
`pytest --html=report.html <path_to_project_tests_folder>/test_phone_book.py` -- Linux
 
