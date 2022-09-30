from ast import Delete
# from curses import raw
from time import sleep
from unittest import result
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
    2: 'Make a task complete',
    3: 'Remove a task',
    4: 'Edit a task',
    5: 'Show all tasks',
    6: 'Exit'
}

# Menu


def print_menu(show_option):

    columns = ["Sel.", "Options"]
    myTable = PrettyTable()

    if (show_option == "All"):
        # Add Columns
        os.system("cls")

        myTable.add_column(
            columns[0], ["1", "2", "3", "4", "5", "6", "7", "8"])
        myTable.add_column(columns[1], [
                           "Add a task", "Make a task complete", "Remove a task", "Edit a task", "Show all tasks", "Show completed tasks", "Show not completed tasks", "Exit"])
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
            show_Tasks("Not completed")
            complete_Task()

        elif menu_selection == "3":
            # Remove a task
            pass
        elif menu_selection == "4":
            # Edit_Tasks("All")
            pass
        elif menu_selection == "5":
            show_Tasks("All")
        elif menu_selection == "6":
            show_Tasks("Completed")
        elif menu_selection == "7":
            show_Tasks("Not completed")
        elif menu_selection == "8":
            # Exit()
            pass

        else:

            print("Invalid selection")
            sleep(2)
            print_menu("All")
    if menu_type != "All":
        if menu_selection == "1":
            print("Add a task")
            add_task()

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
    sql = "INSERT INTO dailyTask (title, explanation,status,date) VALUES (%s, %s,%s,%s)"

    val = (new_task.title, new_task.explanation,
           new_task.status, new_task.date)
    mycursor = mydb.cursor()
    mycursor.execute(sql, val)
    mydb.commit()
    # ****************
    sleep(2)
    print_menu("All")
# To make a task complete, change the status of the task!


def search():
    flag = False
    user_input_Message = "Enter the Id for the task: "
    while (flag == False):

        selection = (input(user_input_Message),)
        mycursor = mydb.cursor()
        mycursor.execute("SELECT * FROM dailyTask WHERE Id LIKE %s", selection)
        myresult = mycursor.fetchall()

        if len(myresult) != 0:
            flag = True
            break
        else:
            user_input_Message = "Wrong Id! Please enter the Id for the task: "
    myTable = PrettyTable()
    myTable.field_names = ["Id", "Title",
                           "What to do", "Status", "Due date"]
    for index in range(len(myresult)):
        myTable.add_row(myresult[index])
    return myTable, selection


def complete_Task():
    mycursor = mydb.cursor()
    print(mycursor)
   # print(selection)
    flag = False
    user_input_message = "Is the task completed? [Y/N]: "
    result = search()
    print(int(result[1][0])+1)
    selection = int(result[1][0])
    res = [result[1][0]]
    print(type(selection))
    print(result[0])
    while flag != True:
        user_input = input(user_input_message)
        if (user_input.lower() == "y" or user_input.lower() == "n"
                or user_input.lower() == "yes" or user_input.lower() == "NO"):
            break
        else:
            print("Wrong answer...")
    if (user_input.lower() == "y"):

        # sql = ("UPDATE dailyTask SET status = 'Done' WHERE Id LIKE %s",
        # (result[1][0]))
        mycursor.execute("UPDATE dailyTask SET status = 'Done' WHERE Id LIKE %s",
                         res)
        mydb.commit()
    else:
        print_menu("All")


def show_Tasks(status):
    mycursor = mydb.cursor()
    if (status == "All"):
        mycursor.execute("SELECT * FROM dailyTask")
    elif (status == "Completed"):
        mycursor.execute("SELECT * FROM dailyTask WHERE status='Done'")
    elif (status == "Not completed"):
        mycursor.execute("SELECT * FROM dailyTask WHERE status='Not Done'")

    myresult = mycursor.fetchall()
    # print(myresult, "<----------")
    myTable = PrettyTable()
    myTable.field_names = ["Id", "Title", "What to do", "Status", "Due date"]

    for index in range(len(myresult)):
        myTable.add_row(myresult[index])

    print(myTable)
    print(len(myresult))

    # print_menu("All")


mycursor = mydb.cursor()


mycursor.execute("SELECT * FROM dailyTask")

myresult = mycursor.fetchall()
if (len(myresult) == 0):

    print_menu("")
else:

    print_menu("All")


# Todo
''' Validation for userinput when the user inputs wrong number '''

# Specify the Column Names while initializing the Table
# Add rows
# print_menu("All")


''' Todo
Check the length of the bank! If the length is greater
Than 0, the menu with all the available alternatives should
calls otherwise the menu with 2 alternatives calls.'''
