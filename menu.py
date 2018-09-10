import csv
import datetime
import os
import re
import sys


class Menu:
    """Set the field names for the headers in the csv and open the menu"""
    def __init__(self):
        self.fieldnames = ['row_number', 'date', 'task', 'minutes', 'notes']
        self.menu()

    def clear(self):
        """Clears the screen"""
        os.system('cls' if os.name == 'nt' else 'clear')

    def menu(self, alert=None):
        """
        Opens the top level menu and provides user
        with available options.  Presents any alerts that are
        sent to indicate successful record completion.
        """
        self.clear()
        if alert:
            print(alert)
        menu_choice = input("Choose:\n"
                            "[A]dd new entry\n"
                            "[L]ook up previous entries\n"
                            "[Q]uit\n\n"
                            ).upper()
        menu_choices = ['A', 'L', 'Q']

        while menu_choice not in menu_choices:
            menu_choice = input("You must select [A] to add "
                                "[L] to look up previous entries "
                                "or [Q] to quit.\n\n"
                                ).upper()
        if menu_choice == "A":
            self.add()
        elif menu_choice == "L":
            if os.path.exists('./entries.csv'):
                self.lookup()
            else:
                self.menu("There are no entries.")
        elif menu_choice == "Q":
            self.quit()

    def take_task(self):
        """
        Takes input from user for task and returns it
        Max length 50, must not be blank
        """
        task_name = input("Task Name:\n ")
        while True:
            if (isinstance(task_name, str)):
                if (len(task_name) < 51) and (len(task_name) > 0):
                    break
                else:
                    task_name = input("Please enter a string for the Task"
                                      " Name (Max Length 50 characters):\n")
            else:
                task_name = input("Please enter a string for the Task Name "
                                  "(Max Length 50 characters):\n")
        return task_name

    def take_min(self):
        """
        Takes input from user for minutes and returns it.
        Must be an integer no longer than 10 digits.
        """
        minutes = input("Number of minutes spent working on task:\n")
        while True:
            if (len(str(minutes)) <= 10):
                try:
                    minutes = int(minutes)

                except ValueError:
                    minutes = input("Please enter an integer for number"
                                    " of minutes (10 digit max):\n")

                else:
                    break
            else:
                minutes = input("Please enter an integer for number of"
                                " minutes (10 digit max):\n")
        return minutes

    def take_notes(self):
        """
        Takes optional notes from user and returns them.
        Max length 500.
        """
        notes = input("Optional additional notes:\n")
        while True:
            if notes is False:
                break
            elif (isinstance(notes, str) and (len(notes) < 501)):
                break
            else:
                notes = input("Please enter a string for Notes"
                              " (Max Length 500 characters):\n")
        return notes

    def take_match(self):
        """
        Takes an input from user to check whether it will match task or notes.
        Returns it.  The difference between this and takes notes is just that
        the input is not optional here.
        """
        match = input("Enter text to search for in task names and notes:\n")
        while True:
            if ((len(match) > 0) and (len(match) < 501)):
                break
            else:
                match = input("Enter text to search for in task names"
                              " and notes (Max Length 500 characters):\n")
        return match

    def take_date(self):
        """
        Takes a date from user in mm/dd/yy format and returns it.
        """
        while True:
            try:
                date = input("Enter date (Must be in mm/dd/yy format):\n")
                date = datetime.datetime.strptime(date, "%m/%d/%y")
                date = date.strftime("%m/%d/%y")
            except ValueError:
                print("Must be in mm/dd/yy format!")
            else:
                break
        return date

    def take_pattern(self):
        """
        Takes an input from user and confirms it is a valid
        regex.  Returns it.
        """
        while True:
            try:
                user_input = input("Enter Valid Regex Pattern to search.\n"
                                   "(Example:r'[YOUR INPUT HERE]')\n")
                pattern = (r'%s' % user_input)
                re.compile(pattern)

            except re.error:
                print(user_input + " is not a valid regex expression")
            else:
                break
        return pattern

    def add(self):
        """
        Adds an entry to csv.  If there is no file named
        entries.csv or no headers they are added.
        task minutes and notes are taken from user.
        Date is set to the current date.
        A row column is also utilized to keep track of records.
        """
        self.clear()
        task_name = self.take_task()
        minutes = self.take_min()
        notes = self.take_notes()

        date = datetime.datetime.now().strftime("%m/%d/%y")
# Check if csv exists yet
        if os.path.exists('./entries.csv'):
            row_count = 0
            with open('entries.csv', newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    row_count += 1

            with open('entries.csv', 'a', newline='') as csvfile:

                entrywriter = csv.DictWriter(csvfile,
                                             fieldnames=self.fieldnames)
                entrywriter.writerow({'row_number': row_count,
                                      'date': date, 'task': task_name,
                                      'minutes': minutes, 'notes': notes})
        else:
            with open('entries.csv', 'a', newline='') as csvfile:
                row_count = 0
                entrywriter = csv.DictWriter(csvfile,
                                             fieldnames=self.fieldnames)
                entrywriter.writeheader()
                entrywriter.writerow({'row_number': row_count,
                                      'date': date, 'task': task_name,
                                      'minutes': minutes, 'notes': notes})
        alert = "Entry Added\n"
        self.menu(alert)

    def lookup(self):
        """
        A lookup enu for the user to select search options
        from.
        """
        self.clear()
        menu_choice = input("How would you like to search:\n"
                            "By [D]ate\n"
                            "By [R]ange of Dates\n"
                            "By [T]ime spent\n"
                            "By [E]xact match\n"
                            "By [P]attern match\n"
                            "[B]ack to previous menu\n"
                            "[Q]uit\n\n"
                            ).upper()
        menu_choices = ['D', 'R', 'T', 'E', 'P', 'B', 'Q']
        while menu_choice not in menu_choices:
            menu_choice = input("You must select [D], [R], [T], [E],"
                                " [P], [B] or [Q] \n"
                                ).upper()
        if menu_choice == 'D':
            if os.path.exists('./entries.csv'):
                self.lookup_date()
            else:
                self.menu("There are no entries")
        elif menu_choice == 'R':
            if os.path.exists('./entries.csv'):
                self.lookup_range()
            else:
                self.menu("There are no entries")
        elif menu_choice == 'T':
            if os.path.exists('./entries.csv'):
                self.lookup_time()
            else:
                self.menu("There are no entries")
        elif menu_choice == 'E':
            if os.path.exists('./entries.csv'):
                self.lookup_match()
            else:
                self.menu("There are no entries")
        elif menu_choice == 'P':
            if os.path.exists('./entries.csv'):
                self.lookup_pattern()
            else:
                self.menu("There are no entries")
        elif menu_choice == 'B':
            self.menu()
        elif menu_choice == 'Q':
            self.quit()

    def lookup_pattern(self):
        """
        Takes pattern from a user and performs a regex search
        on tasks and notes to see if there are matches, Passes
        any found to be paged through.
        """
        self.clear()
        pattern = self.take_pattern()
        with open('entries.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            row_count = 0
            matches = []
            for row in reader:
                if ((re.search(pattern, row['task'])) or
                        (re.search(pattern, row['notes']))):
                    row_count += 1
                    matches.append(row)
                    print(str(row_count) + ". " + row['task'])
        if row_count == 0:
            self.no_pages()
        else:
            self.paging(matches)

    def lookup_range(self):
        """
        Takes two dates from the user, checks if there are any
        dates with entries between those two dates and adds
        the results to a list that the user can page through.
        """
        self.clear()
        self.show_dates()
        print("First Date")
        first_date = self.take_date()
        first_date = datetime.datetime.strptime(first_date, '%m/%d/%y')
        self.clear()
        self.show_dates()
        print("Second Date")
        second_date = self.take_date()
        second_date = datetime.datetime.strptime(second_date, '%m/%d/%y')
        self.clear()
        with open('entries.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            row_count = 0
            matches = []
            for row in reader:
                search_dates = (datetime.datetime.strptime(row['date'],
                                '%m/%d/%y'))
                if ((first_date <= search_dates and
                        second_date >= search_dates) or
                        (first_date >= search_dates and
                         second_date <= search_dates)):

                    row_count += 1
                    matches.append(row)
                    print(str(row_count) + ". " + row['task'])

        if row_count == 0:
            self.no_pages()
        else:
            self.paging(matches)

    def show_dates(self):
        """
        Shows all dates containing entries to the user.
        """
        print("The following dates have entries:\n")
        with open('entries.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            row_count = 0
            all_dates = []
# appends rows to all_dates to prevent doubles showing
            for row in reader:
                if (row['date'] not in all_dates):
                    row_count += 1
                    all_dates.append(row['date'])
                    print(str(row_count) + ". " + row['date'])

    def lookup_date(self):
        """
        Shows user a list of dates with entries.
        Takes date from a user, matches it
        against the csv and sends the matches to
        be presented to the user in pages.
        """
        self.clear()
        self.show_dates()
        date = self.take_date()
        self.clear()
        print("Task Names for \"" + date + "\":\n")
        with open('entries.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            row_count = 0
            matches = []
            for row in reader:
                if (date == row['date']):
                    row_count += 1
                    matches.append(row)
                    print(str(row_count) + ". " + row['task'])

        if row_count == 0:
            self.no_pages()
        else:
            self.paging(matches)

    def lookup_time(self):
        """
        Takes number of minutes to match against csv and
        places matches in a list to be used in the pages
        shown to the user.
        """
        self.clear()
        minutes = self.take_min()
        self.clear()
        print("Task Names with \"" + str(minutes) + "\" minutes spent:\n")
        with open('entries.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            row_count = 0
            matches = []
            for row in reader:
                if (minutes == int(row['minutes'])):
                    row_count += 1
                    matches.append(row)
                    print(str(row_count) + ". " + row['task'])

        if row_count == 0:
            self.no_pages()
        else:
            self.paging(matches)

    def lookup_match(self):
        """
        Takes exact string to match from user and compares it to csv
        task and notes columns. Passes this on to the pages function
        to allow user to scroll through pages of search results.
        """
        self.clear()
        match = self.take_match()

        self.clear()
        print("Task Names and notes with Exact Match Results For \"" +
              match + "\":\n")
        with open('entries.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            row_count = 0
            matches = []
# Checks the input from user against task and notes
# rows from the csv being read
# and saves all row data to matches
            for row in reader:
                if (match in row['task'] or match in row['notes']):
                    row_count += 1
                    matches.append(row)
                    print(str(row_count) + ". " + row['task'])
        if row_count == 0:
            self.no_pages()
        else:
            self.paging(matches)

    def no_pages(self):
        """
        If there are no search results then this
        provides the users that information
        and with their options
        """
        print("\nNo results found")
        menu_choice = input("[M]ain menu\n"
                            "[B]ack to search menu\n"
                            "[Q]uit\n\n"
                            ).upper()
        menu_choices = ['M', 'B', 'Q', 'S']
        while menu_choice not in menu_choices:
            menu_choice = input("You must select [M], [B] or [Q] \n"
                                ).upper()
        if menu_choice == 'M':
            self.menu()
        elif menu_choice == 'B':
            self.lookup()
        elif menu_choice == 'Q':
            self.quit()

    def make_pages(self, matches, match_count):
        """
        Prints all information for one row in the csv
        The information is stored in the matches list
        match_count gives the specific list entry
        """
        print("\nPage For Result " + str((match_count + 1)) + ":\n")
        print("entry id : " + matches[match_count]['row_number'] +
              "\nDate: " + matches[match_count]['date'] + "\n" +
              "Task Name: " + matches[match_count]['task'] +
              "\nMinutes Spent: " + matches[match_count]['minutes'] +
              "\nOptional Notes:" + matches[match_count]['notes'] +
              "\n\n")

    def paging(self, matches):
        """
        Prints the first page of the search results
        and lets users select other results, choose
        to edit or delete them, go back to main
        menu or quit the application
        matches provides the matching csv rows
        """

        match_count = 0
# Stop users from nexting or previousing
# Past the end or beginning of the list
        while True:
            if match_count < 0:
                match_count = 0
                print("\nNo previous results")
            if match_count == len(matches):
                match_count = (len(matches) - 1)
                print("\nNo further results")
# Show all information for selected match
            self.make_pages(matches, match_count)
# Record the entry_number from the csv to edit the csv
            entry_number = matches[match_count]['row_number']
# Add sequential integer for each match
# Incremented by 1 since users count from
# At the same time add all tasks to a new list
# To display as search results
            match_choices = []
            search = []
            for i in range(len(matches)):
                match_number = str(i+1)
                match_choices.append(match_number)
                search.append(match_number + ". " + matches[i]['task'])

            menu_choice = input("Menu Options:\n"
                                "[N]ext Page, "
                                "[P]revious Page,\n"
                                "[E]dit,"
                                "[D]elete,\n"
                                "[M]ain menu, "
                                "[B]ack to search menu, "
                                "[Q]uit\n"
                                "or you can enter the number of a "
                                "search result to jump to its page\n"
                                ).upper()
            menu_choices = ['M', 'B', 'Q', 'E', 'N', 'P', 'D']
# Add numbers for search results to menu choices
            menu_choices.extend(match_choices)
# Let user choose again from the menu
# while showing task names of search results
            while menu_choice not in menu_choices:
                self.clear()

                print("Task Names of Results:\n")
                print("\n".join(search))
                menu_choice = input("You Must Select From:\n"
                                    "[N]ext Page, "
                                    "[P]revious Page,\n"
                                    "[E]dit,"
                                    "[D]elete,\n"
                                    "[M]ain menu, "
                                    "[B]ack to search menu, "
                                    "[Q]uit\n"
                                    "or you can enter the number of a "
                                    "search result to jump to its page\n"
                                    ).upper()
            if menu_choice == 'M':
                self.menu()
            elif menu_choice == 'B':
                self.lookup()
            elif menu_choice == 'S':
                self.lookup_match()
            elif menu_choice == 'N':
                self.clear()
                print("Task Names of Results:\n")
                print("\n".join(search))
                match_count += 1
            elif menu_choice == 'E':
                alteration = "Edit"
                self.alter(entry_number, alteration)
            elif menu_choice == 'P':
                self.clear()
                print("Task Names of Results:\n")
                print("\n".join(search))
                match_count -= 1
            elif menu_choice == 'D':
                alteration = "Delete"
                self.alter(entry_number, alteration)
            elif menu_choice == 'Q':
                self.quit()
# If user enters a search result number send them to its page
# Decrement the users input by one to match list starting at 0
            elif menu_choice in match_choices:
                self.clear()
                print("Task Names of Results:\n")
                print("\n".join(search))
                match_count = (int(menu_choice) - 1)

    def edit(self, row_count, all_entries):
        """
        Asks user if they want to enter new values for values for
        any of the csv fields
        Row Count accesses a list containing all entries in the csv
        at the entry to be edited
        """
        self.clear()
        while True:
            task_check = input("Current Task Name: " +
                               all_entries[row_count]['task'] +
                               "\nOptions:"
                               "\n[L]eave Task Name as is" +
                               "\n[C]hange Task Name\n").upper()
            if task_check == "L":
                self.clear()
                break
            elif task_check == "C":
                all_entries[row_count]['task'] = self.take_task()
                self.clear()
                break
            else:
                self.clear()
                print("You must enter [L] or [C]")
        while True:
            min_check = input("Current Minutes Spent: " +
                              all_entries[row_count]['minutes'] +
                              "\nOptions:"
                              "\n[L]eave Minutes Spent as is" +
                              "\n[C]hange Minutes Spent\n").upper()
            if min_check == "L":
                self.clear()
                break
            elif min_check == "C":
                all_entries[row_count]['minutes'] = self.take_min()
                self.clear()
                break
            else:
                self.clear()
                print("You must enter [L] or [C]")
        while True:
            dates_check = input("Current date for entry: " +
                                all_entries[row_count]['date'] +
                                "\nOptions:"
                                "\n[L]eave Date" +
                                "\n[C]hange Date\n").upper()
            if dates_check == "L":
                self.clear()
                break
            elif dates_check == "C":
                all_entries[row_count]['date'] = self.take_date()
                self.clear()
                break
            else:
                self.clear()
                print("You must enter [L] or [C]")

        while True:
            notes_check = input("Current Optional Notes: " +
                                all_entries[row_count]['notes'] +
                                "\nOptions:"
                                "\n[L]eave Notes as they are" +
                                "\n[C]hange Notes\n").upper()
            if notes_check == "L":
                self.clear()
                break
            elif notes_check == "C":
                all_entries[row_count]['notes'] = self.take_notes()
                self.clear()
                break
            else:
                self.clear()
                print("You must enter [L] or [C]")

    def alter(self, entry_number, alteration):
        """
        Reads in csv file while placing its rows into a list
        If a row is being deleted that row will not be added to the list
        If a row is being edited the edited row will be added to the list
        The edit method is used to take updated values from the user
        The row number for each row will be sequential from one
        An alert message is sent when returning to the main menu
        Entry number indicates the row in the csv to change
        Alteration indicates whether editing or deleting
        """
        with open('entries.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            row_count = 0
            altered = False
            all_entries = []
            for row in reader:
                if ((row['row_number'] == str(entry_number)) and
                        (altered is False)):

                    if alteration == "Delete":
                        alert = "Entry Deleted\n"
                    elif alteration == "Edit":
                        alert = "Edit Complete\n"
                        all_entries.append(dict(row))
                        self.edit(row_count, all_entries)
                        all_entries[row_count]['row_number'] = row_count
                        row_count += 1
                    altered = True
                else:
                    all_entries.append(dict(row))
# Update the row number so that if an entry was deleted there is not a skip
                    all_entries[row_count]['row_number'] = row_count
                    row_count += 1
# Rewrite the csv file with edits or deletions
        with open('entries.csv', 'w', newline='') as csvfile:
            entrywriter = csv.DictWriter(csvfile, fieldnames=self.fieldnames)
            entrywriter.writeheader()
            entrywriter.writerows(all_entries)
# Return to main menu and indicate delete or edit complete
        self.menu(alert)

    def quit(self):
        """
        Quits the program
        """
        sys.exit(0)


# Program wont run automatically if imported
if __name__ == "__main__":
    Menu()
