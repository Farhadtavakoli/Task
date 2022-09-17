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
    else:
        myTable.add_column(columns[0], ["1", "2"])
        myTable.add_column(columns[1], [
                           "Add a task", "Exit"])
    print(myTable)
    print("Select: ")


# Specify the Column Names while initializing the Table
# Add rows
print_menu("not_all")
print_menu("all")
