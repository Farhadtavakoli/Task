from ast import Delete
from time import sleep
import task_module
from prettytable import PrettyTable
import mysql.connector
import os


mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="YAsinbaba2021",
    database="myTasks"
)
print(".............", mydb)

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

    columns = ["Sel.", "Options"]
    myTable = PrettyTable()

    if (show_option == "All"):
        # Add Columns
        os.system("cls")

        myTable.add_column(columns[0], ["1", "2", "3", "4", "5", "6", "7"])
        myTable.add_column(columns[1], [
                           "Add a task", "Remove a task", "Edit a task", "Show all tasks", "Show completed tasks", "Show not completed tasks", "Exit"])
    else:
        os.system("cls")
        myTable.add_column(columns[0], ["1", "2"])
        myTable.add_column(columns[1], [
                           "Add a task", "Exit"])

    print(myTable)
    menu_input(show_option)


# User input for Menu


def menu_input(menu_type):
    menu_selection = input("Select: ")
    task_list = []
    if menu_type == "All":
        if menu_selection == "1":
            print("Add a task")
            add_task()
        elif menu_selection == "2":
            pass
        elif menu_selection == "3":
            pass
        elif menu_selection == "4":
            show_Tasks("All")
        elif menu_selection == "5":
            show_Tasks("Completed")
        elif menu_selection == "6":
            show_Tasks("Not completed")

        else:

            print("Invalid selection")
            sleep(2)
            print_menu("All")
    if menu_type != "All":
        if menu_selection == "1":
            pass
            # add_task()
        elif menu_selection == "5":
            pass
        else:
            print("Invalid selection")
            sleep(2)
            print_menu("")
            # print_menu()


# Add a task
def add_task():
    status = "Not done"
    title = input("Enter a title for the task: ")
    explanation = input("Enter explanation: ")
    date = input("Enter due date: ")
    new_task = task_module.task(title, explanation, "Not Done", date)
    # Saving to the database here
    print(new_task.title, new_task.explanation,
          new_task.status, new_task.date)
    # ****************
    sql = "INSERT INTO task (title, explanation,status,date) VALUES (%s, %s,%s,%s)"

    val = (title, explanation, status, date)
    mycursor = mydb.cursor()
    mycursor.execute(sql, val)
    mydb.commit()
    # ****************
    sleep(2)
    print_menu("All")


def show_Tasks(status):

    mycursor = mydb.cursor()
    if (status == "All"):
        mycursor.execute("SELECT * FROM task")
    elif (status == "Completed"):
        mycursor.execute("SELECT * FROM task WHERE status='Done'")
    elif (status == "Not completed"):
        mycursor.execute("SELECT * FROM task WHERE status='Not Done'")

    myresult = mycursor.fetchall()

    mycursor = mydb.cursor()

    sql = "DELETE FROM task WHERE status = 'Not Done'"

    mycursor.execute(sql)

    mydb.commit()

    myTable = PrettyTable()

    myTable.field_names = ["Title", "What to do", "Status", "Due date"]

    for index in range(len(myresult)):
        myTable.add_row(myresult[index])
        print(myTable)
    print(len(myresult))
    input("Press any key to continue...")
    print_menu("All")


mycursor = mydb.cursor()
mycursor.execute("SELECT * FROM task")
myresult = mycursor.fetchall()
if (len(myresult) == 0):
    print_menu("")
else:
    print_menu("All")


# Specify the Column Names while initializing the Table
# Add rows
# print_menu("All")


''' Todo
Check the length of the bank! If the length is greater 
Than 0, the menu with all the available alternatives should
calls otherwise the menu with 2 alternatives calls.'''
