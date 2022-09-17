from time import sleep
from prettytable import PrettyTable
import os
# Making menu
menu_options = {
    1: 'Add a task',
    2: 'Remove a task',
    3: 'Edit a task',
    4: 'Show all tasks',
    5: 'Exit'
}

# Menu


def print_menu(show_option):
    os.system("cls")
    columns = ["Sel.", "Options"]
    myTable = PrettyTable()

    if (show_option == "all"):
        # Add Columns
        myTable.add_column(columns[0], ["1", "2", "3", "4", "5"])
        myTable.add_column(columns[1], [
                           "Add a task", "Remove a task", "Edit a task", "Show all tasks", "Exit"])
        input("All")
    else:
        myTable.add_column(columns[0], ["1", "2"])
        myTable.add_column(columns[1], [
                           "Add a task", "Exit"])
        input("empty_bank")
    print(myTable)
    input

# User input for Menu


def input(menu_type):
    menu_selection = input("Select: ")
    if menu_type == "All":
        if menu_selection == "1":
            add_task()
        elif menu_selection == "2":
            pass
        elif menu_selection == "3":
            pass
        elif menu_selection == "4":
            pass
        else:
            print("Invalid selection")
            sleep(5)
            print_menu()
    else:
        if menu_selection == "1":
            add_task()
        elif menu_selection == "5":
            pass
        else:
            print("Invalid selection")
            print_menu()


# Add a task
def add_task(title, explanation, status, date):

    task = {"title": title, "explanation": explanation,
            "status": status, "date": date}

    print(task)


# Specify the Column Names while initializing the Table
# Add rows
print_menu("All")
