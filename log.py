from collections import OrderedDict
import datetime
import os
import sys

from peewee import *

db = SqliteDatabase('entries.db')

# Create the database table
class Entry(Model):

    name = CharField(max_length=255)
    task = CharField(max_length=255)
    minutes = IntegerField()
    notes = TextField()
    timestamp = DateTimeField(default = datetime.datetime.today().strftime('%Y-%m-%d'))

    class Meta:
        database = db


# Clear the screen
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

# Initialize the database
def initialize():
    db.connect()
    db.create_tables([Entry], safe=True)

# Main menu for users to add or view entries
def menu_loop():
    """Show the menu"""
    menu = OrderedDict([
    ('a', "Add Entry"),
    ('v', "View Entries"),
    ('t', "Search by Term"),
    ('p', "Search by Employee"),
    ('m', "Search by Entry Minutes Taken"),
    ('s', "Search by Entry Date"),
    ('r', "Search by Date Range")
    ])
    choice = None

    while choice != 'q':
        clear()
        print("Enter 'q' to quit.")
        for key, value in menu.items():
            print('{}) {}'.format(key, value))
        choice = input('Action: ').lower().strip()

        if choice in menu.keys():
            clear()
            if choice == 'a':
                add_entry()
            if choice == 'v':
                view_entries()
            if choice == 't':
                search_term()
            if choice == 'p':
                search_employee(Entry.select().where(Entry.name.contains(prep_employee_search(Entry.select().order_by(
                                Entry.timestamp.desc())))), prep_employee_search(Entry.select().order_by(
                                Entry.timestamp.desc())))
            if choice == 'm':
                search_minutes()
            if choice == 's':
                search_date()
            if choice == 'r':
                search_range()

# Take a string for names and tasks
def take_string(message):
    while True:
        your_string = input(message)
        if your_string:
            break
        else:
            clear()
    return your_string

# Take an integer for minutes
def take_minutes(message):
    while True:
        try:
            your_minutes = input(message)
            your_minutes = int(your_minutes)
        except ValueError:
            print("Please enter an integer.")
        else:
            break
    return your_minutes

# Takes a date from a user
def take_date():
    """
    Takes a date from user in mm/dd/yy format and returns it.
    """
    while True:
        try:
            date = input("Enter date (Must be in YYYY-mm-dd format):\n")
            date = datetime.datetime.strptime(date, '%Y-%m-%d')
        except ValueError:
            print("Must be in YYYY-mm-dd format!")
        else:
            break
    return date

# Takes all entry fields except date
def take_entry():
    your_name = take_string(
                "\n[REQUIRED] Enter your name: ")
    your_task = take_string(
                "\n[REQUIRED] Enter task name: ")
    your_minutes = take_minutes("\n[INTEGER REQUIRED]"
                        " Minutes the task took: ")
    your_notes = input("\n[OPTIONAL] Enter any notes: ")
    return your_name, your_task, your_minutes, your_notes

# Create an entry with user input and the date
def add_entry():
    """Add an entry."""
    your_name, your_task, your_minutes, your_notes = take_entry()
    if input('Save? [Y/N]').lower() != 'n':
        Entry.create(name=your_name, task=your_task,
                     minutes=your_minutes, notes=your_notes)
        print("Saved")

# Returns a list with a count of entries
def count_ids(entries):
    id_count = []
    count = 0
    for entry in entries:
        id_count.append(count)
        count += 1
    return id_count
# Places the correct query results in entries based on
# query and method
def search_method(entries, search_query, method):

    if search_query and method == "Term":
        entries = (entries.where((Entry.task.contains(search_query)) | (Entry.notes.contains(search_query))))

    elif search_query and method == "Employee":
        entries = (entries.where(Entry.name.contains(search_query)))

    elif search_query and method == "Minutes":
        entries = (entries.where(Entry.minutes == (search_query)))

    elif search_query and method == "Date":
        entries = (entries.where(Entry.timestamp == (search_query)))

    elif search_query and method == "Range":
        entries = (entries.where((Entry.timestamp >= (search_query[0])) &
                  (Entry.timestamp <= (search_query[1]))))
    return entries

# Paginates resultant search entries pending
# Search query and method
def view_entries(search_query=None, method=None):
    """View previous entries."""

    entry_count = 0
    entries = Entry.select().order_by(Entry.timestamp.desc())
    id_count = count_ids(entries)

    while True:

        if (not search_query) and (not method):
            entries = Entry.select().order_by(Entry.timestamp.desc())
            id_count = count_ids(entries)
        else:
            entries = search_method(entries, search_query, method)
            id_count = count_ids(entries)

        if not entries:
            input("No Results, press any key to go back: ")
            break

        elif entries:
            entry = entries[entry_count]
            timestamp = entry.timestamp.strftime('%B %d, %Y')
            clear()
            print("Result Task Names:")
            results_count = 0
            for result_entry in entries:
                results_count += 1
                print(str(results_count) + ".",
                      result_entry.task)

            print ("\nPage ", entry_count +1)
            print(timestamp)
            print('='*len(timestamp))
            print("ID: ", entry.id)
            print("Name: ", entry.name)
            print("Task Name: ", entry.task)
            print("Number of minutes: ", entry.minutes)
            print("Notes: ", entry.notes)
            print('\n' + '='*len(timestamp))
            if entry == entries[-1]:
                print("No Further Pages")
            else:
                print('N) next entry')
            if entry == entries[0]:
                print("No Previous Pages")
            else:
                print('P) previous entry')
            print('Enter a result\'s number to access its page')

            print('q) return to main menu')
            print('d) delete entry')
            print('e) edit entry')

            method = None
            next_action = input('Action: ').lower().strip()
            if next_action == 'q':
                break
            elif next_action == 'n':
                if entry == entries[-1]:
                    pass
                else:
                    entry_count += 1
            elif next_action == 'p':
                if entry == entries[0]:
                    pass
                else:
                    entry_count -= 1

            elif next_action == 'd':
                delete_entry(entry)
                if entry_count > 0:
                    entry_count -= 1
            elif next_action == 'e':
                edit_entry(entry)
            elif next_action:
                try:
                    int(next_action)
                except ValueError:
                    pass
                else:
                    if int(next_action) - 1 in id_count:
                        entry_count = int(next_action) - 1

# Removes an entry
def delete_entry(entry):
    """Delete an entry."""
    if input("Sure? [y/n]").lower() == 'y':
        entry.delete_instance()

# Asks a user to enter new inputs for an entry
def edit_entry(entry):
    """edit an entry."""
    if input("Sure? [y/n]").lower() == 'y':
        your_name, your_task, your_minutes, your_notes = take_entry()
        entry.timestamp = take_date()
        entry.name = your_name
        entry.task = your_task
        entry.minutes = your_minutes
        entry.notes = your_notes
        entry.save()

# Takes a string to search tasks and notes
def search_term():
    """search by term"""
    while True:
        clear()
        search = input('search query: ')
        if search:
            break
    view_entries(search, "Term")

# Shows all employee names
def get_employee_names(entries):
    employees = []
    for result_entry in entries:
        employee = (result_entry.name)
        if employee not in employees:
            employees.append(employee)
    return employees

# Shows list of employee names and takes
# a search term
def prep_employee_search(entries):
    """search employees"""
    clear()
    employees = get_employee_names(entries)
    print("Employee Names:")
    employee_count = 0
    for employee in employees:
        employee_count +=1
        print(str(employee_count) + ".", employee)

    while True:
        search = input('Enter name to search: ')
        if search:
            break
        else:
            print("Please enter Name to search")
    return search

# Gives user a list of employee names
# Takes a name from the user and asks if they
# want to see a list of matching names to search
# Passes resulting search back to be viewed with
# the search employee flag
def search_employee(entries, search):
    employees = get_employee_names(entries)
    id_count = count_ids(employees)
    if len(id_count) > 1:
        check = input("There are multiple employees with this name"
              "\nEnter M to see a list of possible matches"
              "\nOr enter anything else to see all search results.").lower()
        if check == "m":
            clear()
            print("Matching Employee Names:")
            employees = []
            results_count = 0
            for result_entry in entries:
                employee = (result_entry.name)
                if employee not in employees:
                    employees.append(employee)
            for employee in employees:
                results_count +=1
                print(str(results_count) + ".", employee)

            while True:
                search = input('Enter name to search: ')
                if search:
                    break
                else:
                    print("Please enter Name to search")
            view_entries(search, "Employee")
        else:
            view_entries(search, "Employee")
    else:
        view_entries(search, "Employee")



# Prints a list of the minutes that tasks have taken
# Takes an integer for minutes to search
# passes the integer back with the search minutes
# flag
def search_minutes():
    """search by minutes spent"""
    entries = Entry.select()
    clear()
    print("Minutes spent working:")
    employee_mins = []
    results_count = 0
    for result_entry in entries:
        mins = (result_entry.minutes)
        if mins not in employee_mins:
            employee_mins.append(mins)
    for min in employee_mins:
        results_count+=1
        print("{}.".format(results_count), min)

    while True:
        try:
            search_minutes = input("\n[INTEGER REQUIRED]"
                                 "Search Minutes the task took: ")
            search_minutes = int(search_minutes)
        except ValueError:
            print("Please enter an integer.")
        else:
            break

    view_entries(search_minutes, "Minutes")

# Takes a date and passes it with the Date flag
def search_date():
    """search by date"""
    view_entries(take_date(), "Date")

# Takes dates and passes them to the view_entries function in a list
# with the Range flag
def search_range():
    """Search by date range"""
    print("First Date [Must be the earlier date]")
    first_date = take_date()
    print("Second Date [Must be the later date]")
    second_date = take_date()
    dates = [first_date, second_date]
    view_entries(dates, "Range")

if __name__ == '__main__':
    initialize()
    menu_loop()
