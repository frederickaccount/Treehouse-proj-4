import datetime
import unittest
from unittest import TestCase, mock
from unittest.mock import patch

from peewee import *

import log

db = SqliteDatabase('testentries.db')

class Entry(Model):

    name = CharField(max_length=255)
    task = CharField(max_length=255)
    minutes = IntegerField()
    notes = TextField()
    timestamp = DateTimeField(default = datetime.datetime.today().strftime('%Y-%m-%d'))

    class Meta:
        database = db



class LogTests(TestCase):

    def setUp(self):
        db.create_tables([Entry], safe=True)
        check = Entry.select().order_by(Entry.timestamp.desc())

        Entry.get_or_create(name="your_name", task="your_task",
                     minutes=12, notes="your_notes")
        Entry.get_or_create(name="unique", task="your_task2",
                     minutes=123, notes="your_notes2")
        self.entries = Entry.select().order_by(Entry.timestamp.desc())
        self.entry = self.entries[0]


    def test_clear(self):
        with mock.patch('os.system') as mock_clear:
            log.clear()
            mock_clear.assert_called()

    def test_take_entry(self):
        user_input = ['test']
        with patch('builtins.input', side_effect=user_input):
            with mock.patch('log.take_string') as mock_string:
                with mock.patch('log.take_minutes') as mock_mins:
                    log.take_entry()
                    mock_string.assert_called()


    # def test_initialize(self):
    #     with mock.patch('log.db.connect') as mock_init:
    #         log.initialize()
    #         mock_init.assert_called()


    # def test_add_entry(self):
    #     user_input = ['n']
    #     with patch('builtins.input', side_effect=user_input):
    #         with mock.patch('log.take_entry') as mock_entry:
    #             log.add_entry()
    #             mock_entry.assert_called()

    def test_add_entry(self):
        user_input = ['add name', 'add task', '12', 'add notes', 'y']
        with patch('builtins.input', side_effect=user_input):
            with mock.patch('builtins.print', side_effect=print) as mock_print:
                msg = "Saved"
                log.add_entry()
                mock_print.assert_called_with(msg)



    def test_menu_loop_search_employee(self):
        user_input = ['p','q']
        with patch('builtins.input', side_effect=user_input):
            with mock.patch('log.prep_employee_search') as mock_prep:
                with mock.patch('log.search_employee') as mock_search:
                    log.menu_loop()
                    mock_prep.assert_called()
                    mock_search.assert_called()


    def test_menu_loop_search_mins(self):
        user_input = ['m','q']
        with patch('builtins.input', side_effect=user_input):
            with mock.patch('log.search_minutes') as mock_min:
                log.menu_loop()
                mock_min.assert_called()

    def test_menu_loop_search_date(self):
        user_input = ['s','q']
        with patch('builtins.input', side_effect=user_input):
            with mock.patch('log.search_date') as mock_date:
                log.menu_loop()
                mock_date.assert_called()

    def test_menu_loop_search_range(self):
        user_input = ['r','q']
        with patch('builtins.input', side_effect=user_input):
            with mock.patch('log.search_range') as mock_range:
                log.menu_loop()
                mock_range.assert_called()

    def test_take_string(self):
        user_input = ['test']
        with patch('builtins.input', side_effect=user_input):
            test_string = log.take_string("arbitrary")
            self.assertEqual(user_input[0], test_string)

    def test_take_minutes(self):
        user_input = ['12']
        with patch('builtins.input', side_effect=user_input):
            test_mins = log.take_minutes("arbitrary")
            self.assertEqual(int(user_input[0]), test_mins)

    def test_take_minutes_except(self):
        user_input = ['', '12']
        with patch('builtins.input', side_effect=user_input):
            with mock.patch('builtins.print', side_effect=print) as mock_print:
                msg = "Please enter an integer."
                log.take_minutes("arbitrary")
                mock_print.assert_called_with(msg)



    def test_take_string_clear(self):
        user_input = ['','q']
        with patch('builtins.input', side_effect=user_input):
            with mock.patch('os.system') as mock_clear:
                log.take_string("arbitrary")
                mock_clear.assert_called()

    # def test_except_minutes(self):
    #     user_input = ['onetwo']
    #     with patch('builtins.input', side_effect=user_input):
    #         with self.assertRaises(ValueError):
    #             test_mins = log.take_minutes


    def test_take_date(self):
        user_input = ['1234-12-12']
        with patch('builtins.input', side_effect=user_input):
            test_date = log.take_date()
            self.assertEqual(user_input[0], test_date.strftime('%Y-%m-%d'))

    def test_take_date_except(self):
        user_input = ['q', '1234-12-12']
        with patch('builtins.input', side_effect=user_input):
            with mock.patch('builtins.print', side_effect=print) as mock_print:
                msg = "Must be in YYYY-mm-dd format!"
                log.take_date()
                mock_print.assert_called_with(msg)



    def test_count_ids(self):
        example = ['a','b', 'c']
        return_value = log.count_ids(example)
        self.assertEqual(return_value, [0,1,2])

    #
    def test_not_delete_entry(self):
        user_input = ['n']
        flag = 0
        test_entry = self.entry
        with patch('builtins.input', side_effect=user_input):
            log.delete_entry(test_entry)
            test_entries = Entry.select().order_by(Entry.timestamp.desc())
            test_entry = test_entries[0]
            if test_entry == self.entry:
                flag = 1
            self.assertEqual(flag,True)

    def test_delete_entry(self):
        user_input = ['y']
        test_entry = self.entry
        with patch('builtins.input', side_effect=user_input):
            log.delete_entry(test_entry)
            test_entries = Entry.select().order_by(Entry.timestamp.desc())
            test_entry = test_entries[0]
            self.assertNotEqual(test_entry,self.entry)


    def test_not_edit(self):
        user_input = ['n']
        with patch('builtins.input', side_effect=user_input):
            with mock.patch('log.take_entry') as mock_take:
                log.edit_entry(self.entry)
                mock_take.assert_not_called()

    def test_edit(self):
        user_input = ['y','a','b','12','12','1234-12-12']


        with patch('builtins.input', side_effect=user_input):
            entries = Entry.select()
            log.edit_entry(entries[0])
            first_entry = entries[0]

        user_input2 = ['y','z','z','12','12','1234-12-12']
        with patch('builtins.input', side_effect=user_input2):
            entries = Entry.select()
            log.edit_entry(entries[0])
            second_entry = entries[0]

        self.assertNotEqual(first_entry.name, second_entry.name)

    def test_search_term(self):
        user_input = ['test']
        with patch('builtins.input', side_effect=user_input):
            with mock.patch('log.view_entries') as mock_term:
                log.search_term()
                mock_term.assert_called()

    # def test_employee_names(self):
    #     employee_test = log.get_employee_names(self.entries)
    #     self.assertEqual(employee_test,['your_name', 'your_name2', 'your_name3'] )


    def test_view_entries_del(self):
        user_input = ['d','q']
        with patch('builtins.input', side_effect=user_input):
            with mock.patch('log.delete_entry') as mock_del:
                log.view_entries()
                mock_del.assert_called()


    def test_prep_employee_search(self):
        user_input = ['test']
        with patch('builtins.input', side_effect=user_input):
            prep_test = log.prep_employee_search(self.entries)
            self.assertEqual(prep_test, user_input[0])

    def test_prep_employee_else(self):
        user_input = ['', 'ok']
        with patch('builtins.input', side_effect=user_input):
            with mock.patch('builtins.print', side_effect=print) as mock_print:
                msg = "Please enter Name to search"
                log.prep_employee_search(self.entries)
                mock_print.assert_called_with(msg)

    def test_search_employee(self):
        user_input = ['search']
        with patch('builtins.input', side_effect=user_input):
            with mock.patch('log.view_entries') as mock_view:
                log.search_employee(self.entries, "arbitrary")
                mock_view.assert_called()

    def test_unique_search_employee(self):
        search = "your_name2"
        example = Entry.select().where(Entry.name.contains(search))
        with mock.patch('log.view_entries') as mock_view:
            log.search_employee(example, search)
            mock_view.assert_called()

    def test_search_employee_print(self):
        user_input = ['m','', 'your_name']
        with patch('builtins.input', side_effect=user_input):
            with mock.patch('builtins.print', side_effect=print) as mock_print:
                msg = "Please enter Name to search"
                with mock.patch('log.view_entries') as mock_view:
                    log.search_employee(self.entries, "your_name")
                    mock_print.assert_called_with(msg)
                    mock_view.assert_called()

    def test_search_minutes(self):
        user_input = ['string','12']
        with patch('builtins.input', side_effect=user_input):
            with mock.patch('builtins.print', side_effect=print) as mock_print:
                msg = "Please enter an integer."
                with mock.patch('log.view_entries') as mock_view:
                    log.search_minutes()
                    mock_print.assert_called_with(msg)
                    mock_view.assert_called()

    def test_search_date(self):
        user_input=['1234-12-12']
        with patch('builtins.input', side_effect=user_input):
            with mock.patch('log.view_entries') as mock_view:
                log.search_date()
                mock_view.assert_called()

    def test_search_range(self):
        user_input=['1234-12-12', '1234-12-12']
        with patch('builtins.input', side_effect=user_input):
            with mock.patch('log.view_entries') as mock_view:
                log.search_range()
                mock_view.assert_called()


    def test_menu_loop_add(self):
        user_input=['a','q']
        with patch('builtins.input', side_effect=user_input):
            with mock.patch('log.add_entry') as mock_add:
                log.menu_loop()
                mock_add.assert_called()

    def test_menu_loop_view(self):
        user_input=['v','q']
        with patch('builtins.input', side_effect=user_input):
            with mock.patch('log.view_entries') as mock_view:
                log.menu_loop()
                mock_view.assert_called()

    def test_menu_loop_search(self):
        user_input=['t','q']
        with patch('builtins.input', side_effect=user_input):
            with mock.patch('log.search_term') as mock_search:
                log.menu_loop()
                mock_search.assert_called()
if __name__ == '__main__':
    unittest.main()
