#!/usr/bin/env python

from collections import OrderedDict
import datetime
import os
import sys

from peewee import *

db = SqliteDatabase('diary.db')


class Entry(Model):

    name = CharField(max_length=255)
    task = CharField(max_length=255)
    minutes = IntegerField()
    notes = TextField()
    timestamp = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = db


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def initialize():
    db.connect()
    db.create_tables([Entry], safe=True)

def menu_loop():
    """Show the menu"""
    choice = None

    while choice != 'q':
        clear()
        print("Enter 'q' to quit.")
        for key, value in menu.items():
            print('{}) {}'.format(key, value.__doc__))
        choice = input('Action: ').lower().strip()

        if choice in menu:
            clear()
            menu[choice]()


def add_entry():
    """Add an entry."""

    while True:
        your_name = input("\n[REQUIRED] Enter your name: ")
        if your_name:
            break
    while True:
        your_task = input("\n[REQUIRED] Enter task name: ")
        if your_task:
            break
    while True:
        try:
            your_minutes = input("\n[INTEGER REQUIRED]"
                                 " Minutes the task took: ")
            your_minutes = int(your_minutes)
        except ValueError:
            print("Please enter an integer.")
        else:
            break
    print("\n[OPTIONAL] Enter your notes. Press"
          " ctrl+d when finished (ctrl+z for windows).")

    your_notes = sys.stdin.read().strip()

    if input('Save? [Y/N]').lower() != 'n':
        Entry.create(name=your_name, task=your_task,
                     minutes=your_minutes, notes=your_notes)
        print("Saved")


def view_entries(search_query=None):
    """View previous entries."""

    entries = Entry.select().order_by(Entry.timestamp.desc())

    if search_query:
        entries = entries.where(Entry.content.contains(search_query))

    for entry in entries:
        timestamp = entry.timestamp.strftime('%A %B %d, %Y %I:%M%p')
        clear()
        print(timestamp)
        print('='*len(timestamp))
        print(entry.content)
        print('\n\n' + '='*len(timestamp))
        print('N) next entry')
        print('q) return to main menu')
        print('d) delete entry')

        next_action = input('Action: [N/Q] ').lower().strip()
        if next_action == 'q':
            break
        elif next_action == 'd':
            delete_entry(entry)

def delete_entry(entry):
    """Delete an entry."""
    if input("Sure? [y/n]").lower() == 'y':
        entry.delete_instance()


def search_entries():
    """search entries """
    view_entries(input('search query: '))



menu = OrderedDict([
('a', add_entry),
('v', view_entries),
('d', delete_entry)
('s', search_entries)
]

)


if __name__ == '__main__':
    initialize()
    menu_loop()
