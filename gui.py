import tkinter as tk
from tkinter import ttk
from database import add_task, get_tasks, create_table
from scraper import import_tasks
import dropbox
import os

# Dropbox API key
DROPBOX_ACCESS_TOKEN = 'your_dropbox_access_token_here'


def on_add_task():
    course = course_entry.get()
    task_type = task_type_combobox.get()
    deadline = deadline_entry.get()
    if course and task_type and deadline:
        add_task(course, task_type, deadline)
        load_tasks()


def load_tasks():
    for row in tree.get_children():
        tree.delete(row)
    tasks = get_tasks()
    for task in tasks:
        tree.insert("", tk.END, values = task)


def on_pull_tasks():
    import_tasks()
    load_tasks()


def save_to_dropbox():
    dbx = dropbox.Dropbox(DROPBOX_ACCESS_TOKEN)
    with open('tasks.db', 'rb') as f:
        dbx.files_upload(f.read(), '/tasks.db', mode = dropbox.files.WriteMode.overwrite)
    print("Database saved to Dropbox")


def download_from_dropbox():
    dbx = dropbox.Dropbox(DROPBOX_ACCESS_TOKEN)
    with open('tasks.db', 'wb') as f:
        metadata, res = dbx.files_download(path = '/tasks.db')
        f.write(res.content)
    print("Database downloaded from Dropbox")
    load_tasks()


def create_gui():
    root = tk.Tk()
    root.title("University Task Manager")
    root.geometry("800x600")
    root.resizable(False, False)

    # Frames
    left_frame = tk.Frame(root, width = 200, bg = 'lightgrey')
    center_frame = tk.Frame(root, width = 400)
    right_frame = tk.Frame(root, width = 200, bg = 'lightgrey')
    left_frame.pack(side = "left", fill = "y")
    center_frame.pack(side = "left", fill = "both", expand = True)
    right_frame.pack(side = "right", fill = "y")

    # Left frame widgets for adding a new task
    global course_entry, task_type_combobox, deadline_entry, tree
    tk.Label(left_frame, text = "Course").pack(pady = 5)
    course_entry = tk.Entry(left_frame)
    course_entry.pack(pady = 5)

    tk.Label(left_frame, text = "Task Type").pack(pady = 5)
    task_type_combobox = ttk.Combobox(left_frame,
                                      values = ['laboratory work', 'practical work', 'individual work', 'project'])
    task_type_combobox.pack(pady = 5)

    tk.Label(left_frame, text = "Deadline (YYYY-MM-DD)").pack(pady = 5)
    deadline_entry = tk.Entry(left_frame)
    deadline_entry.pack(pady = 5)

    tk.Button(left_frame, text = "Add Task", command = on_add_task).pack(pady = 20)

    tk.Button(left_frame, text = "Login and pull tasks from ELSE", command = on_pull_tasks).pack(pady = 20)

    tk.Button(left_frame, text = "Save the database to Dropbox", command = save_to_dropbox).pack(pady = 20)

    tk.Button(left_frame, text = "Download the database from Dropbox", command = download_from_dropbox).pack(pady = 20)

    # Center frame for displaying tasks
    columns = ("id", "course", "task_type", "stage1_status", "stage2_status", "stage3_status", "deadline")
    tree = ttk.Treeview(center_frame, columns = columns, show = 'headings')
    for col in columns:
        tree.heading(col, text = col)
    tree.pack(fill = "both", expand = True)

    # Right frame for notifications and settings
    tk.Label(right_frame, text = "Notifications", bg = 'lightgrey').pack(pady = 10)
    tk.Label(right_frame, text = "Settings", bg = 'lightgrey').pack(pady = 10)

    load_tasks()
    root.mainloop()
