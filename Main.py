from ast import Delete
from sqlite3 import Cursor
# from curses import raw
from time import sleep
from turtle import title
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

    if menu_type == "All":
        if menu_selection == "1":
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
            task = update_database()
            if (len(task) > 0):
                remove_task(task)
            else:
                print("No data to delete...")
                sleep(1)
                print_menu("")

        elif menu_selection == "4":
            task = update_database()
            edit_task(task)
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
    if (len(update_database()) == 0):
        sql = "ALTER TABLE dailyTask AUTO_INCREMENT = 100"
        mycursor = mydb.cursor()
        mycursor.execute(sql)
        mydb.commit()
    status = "Not done"
    title = ""
    explanation = ""
    date = ""
    while title == "":
        title = input("Enter a title for the task: ")
        title = title.strip()
    while explanation == "":
        explanation = input("Enter explanation: ")
        explanation = explanation.strip()
    # TODO Add a date validation here
    while date == "":
        date = input("Enter due date: ")
        date = date.strip()
    new_task = task_module.task(title, explanation, status, date)
    # Saving to the database here
    print("The new task is saved as ", new_task.title)
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


def find_id(task):
    id_flag = False
    global id
    task_id_selection = "Enter the Id for the task: "

    while id_flag != True:
        selection = input(task_id_selection)
        selection = selection.strip()
        if selection == "":
            continue
        selection = int(selection)
        for index in range(len(task)):
            if (selection) == task[index][0]:
                id = task[index][0]
                id_flag = True
        task_id_selection = "Wrong Id task! Enter the Id for the task please: "
    return id


def remove_task(task):
    flag = False
    mycursor = mydb.cursor()
    show_Tasks("All", "edit")
    id = find_id(task)
    remove_question = "Do you want to delete the task? [Y/N]: "
    while flag != True:
        user_input = input(remove_question)
        if (user_input.lower() == "y" or user_input.lower() == "n"
                or user_input.lower() == "yes" or user_input.lower() == "NO"):
            break
        else:
            print("Wrong answer...")
    if (user_input.lower() == "y"):
        mycursor.execute("DELETE FROM dailyTask WHERE Id LIKE %s",
                         ("%" + str(id) + "%",))
        mydb.commit()
        input("The task is now deleted. Press the Enter key please...")
        print_menu("All")
    else:
        print_menu("All")


def complete_Task(task):
    mycursor = mydb.cursor()
    flag = False
    global id
    is_task_completed = "Do you want to complete the task ? [Y/N]: "
    id = find_id(task)
    while flag != True:
        user_input = input(is_task_completed)
        if (user_input.lower() == "y" or user_input.lower() == "n"
                or user_input.lower() == "yes" or user_input.lower() == "NO"):
            break
        else:
            print("Wrong answer...")
    if (user_input.lower() == "y"):
        mycursor.execute("UPDATE dailyTask SET status = 'Done' WHERE Id LIKE %s",
                         ("%" + str(id) + "%",))
        input("The task is now completed. Press the Enter key please...")
        print_menu("All")
        mydb.commit()
        update_database()
    else:
        print_menu("All")


def edit_task(task):
    show_Tasks("All", "edit")

    id = (find_id(task))
    title = ""
    explanation = ""
    date = ""
    while title == "":
        title = input("Enter new title for the task: ").strip()

    while explanation == "":
        explanation = input("Enter new explanation for the task: ").strip()
    while date == "":
        date = input("Enter new due date for the task: ").strip()

    mycursor = mydb.cursor()
    sql = ("UPDATE dailyTask SET title=%s , explanation=%s, date=%s WHERE Id=%s")
    print(sql)
    val = (title, explanation, date, id)
    mycursor.execute(sql, val)
    print("Changes are saved to the bank")
    input("Press enter key to continue...")
    print_menu("All")
    #[id, title, explanation, status, date, id]
    mydb.commit()
    update_database()
    mycursor.close()
    mydb.close()


def show_Tasks(status, type):
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM dailyTask")

    if (status == "All"):
        mycursor.execute("SELECT * FROM dailyTask")
    elif (status == "Completed"):
        mycursor.execute("SELECT * FROM dailyTask WHERE status='Done'")
    elif (status == "Not completed"):
        mycursor.execute("SELECT * FROM dailyTask WHERE status='Not Done'")

    myresult = mycursor.fetchall()
    myTable = PrettyTable()
    myTable.field_names = ["Id", "Title", "What to do", "Status", "Due date"]

    for index in range(len(myresult)):
        myTable.add_row(myresult[index])

    if (len(myresult) > 0 and type == "complete"):
        print(myTable)
        complete_Task(myresult)
        print_menu("All")

    elif (len(myresult) > 0 and type == "remove" or type == "edit"):
        print(myTable)

    elif (len(myresult) > 0):
        print(myTable)
        input("Press Enter key please...")
        print_menu("All")

    else:
        print("There is no task to do or no task in daily tasks")
        sleep(2)
        print_menu("All")

    return len(myresult), myresult


def update_database():
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM dailyTask")
    task = mycursor.fetchall()
    return task


update_database()
if (len(update_database()) == 0):
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
