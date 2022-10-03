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
            uncompleted_tasks = show_Tasks("Not completed", "complete")

            if (uncompleted_tasks[0] > 0):
                pass
            else:
                print("There is no uncompleted task.")
                sleep(2)
                print_menu("All")

        elif menu_selection == "3":
            # Remove a task
            pass
        elif menu_selection == "4":
            # Edit_Tasks("All")
            pass
        elif menu_selection == "5":
            show_Tasks("All", "show")
        elif menu_selection == "6":
            show_Tasks("Completed", "show")
        elif menu_selection == "7":
            show_Tasks("Not completed", "show")
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

        selection = int(input(user_input_Message))
        print(type(selection))
        mycursor = mydb.cursor()
        mycursor.execute("SELECT * FROM dailyTask WHERE status='Not Done'")
        myresult = mycursor.fetchall()
        print(myresult)
        print(len(myresult))
        print("...............")
        print(type(selection))
        print(type(myresult[0][0]))

        for index in range(len(myresult)):
            if (selection == myresult[index][0]):
                print("Found it on place ", index)
                # mycursor.execute(
                # "SELECT * FROM dailyTask WHERE Id LIKE (%s)", selection)

            else:
                print(
                    "The Id number you entered is not in the uncompleted tasks' Id numbers")
                sleep(2)
                search()
            myresult = mycursor.fetchall()

        if len(myresult) != 0:
            flag = True

            break
        elif len(myresult) == 0:
            print("There is no uncompleted tasks in the bank.")
        else:
            user_input_Message = "Wrong Id! Please enter the Id for the task: "
    myTable = PrettyTable()
    myTable.field_names = ["Id", "Title",
                           "What to do", "Status", "Due date"]
    for index in range(len(myresult)):
        myTable.add_row(myresult[index])
    return myTable, selection


def complete_Task(task):
    flag = False
    id_flag = False
    global id
    is_task_completed = "Do you want to complete the task ? [Y/N]: "
    task_id_selection = "Enter the Id for the task: "

    while id_flag != True:

        selection = int(input(task_id_selection))
        if selection == "":
            continue

    #result = search()
        for index in range(len(task)):
            if (selection) == task[index][0]:
                id = task[index][0]
                id_flag = True
                print("Your task for ", task[index][1], " is not done yet.")
        task_id_selection = "Wrong Id task! Enter the Id for the task please: "

    while flag != True:
        user_input = input(is_task_completed)
        if (user_input.lower() == "y" or user_input.lower() == "n"
                or user_input.lower() == "yes" or user_input.lower() == "NO"):
            break
        else:
            print("Wrong answer...")
    if (user_input.lower() == "y"):

       # sql = ("UPDATE dailyTask SET status = 'Done' WHERE Id LIKE %s",
        # id)
        #print("---------------->", sql)

        mycursor.execute("UPDATE dailyTask SET status = 'Done' WHERE Id LIKE %s",
                         ("%" + str(id) + "%",))
        input("The task is now completed. Press the Enter key please...")
        print_menu("All")
        mydb.commit()
    else:
        print_menu("All")


def show_Tasks(status, type):
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM dailyTask")
    if (len(mycursor.fetchall()) > 0):
        flag = True
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

    if (len(myresult) > 0 and type == "complete"):
        print(myTable)
        complete_Task(myresult)
        print_menu("All")
    elif (len(myresult) > 0):
        print(myTable)
        input("Press Enter key please...")
        print_menu("All")

    else:
        print("No record to show")
        sleep(2)
        print_menu("All")

    return len(myresult), myresult

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
