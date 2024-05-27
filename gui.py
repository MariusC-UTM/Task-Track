import tkinter as tk
from tkinter import ttk
from database import add_task, get_tasks, create_table
from scraper import import_tasks
import dropbox
import os


def read_dropbox_token():
    token_file_path = os.path.join('private user data', 'dropbox_api_token.txt')
    with open(token_file_path, 'r') as file:
        return file.read().strip()


# Read the Dropbox API key from the file
DROPBOX_ACCESS_TOKEN = read_dropbox_token()


def on_add_task():
    course = course_entry.get()
    task_type = task_type_combobox.get()
    deadline = deadline_entry.get()
    number = number_entry.get() if task_type == 'laboratory work' or task_type == 'practical work' else None
    if course and task_type and deadline:
        add_task(course, task_type, deadline, number)
        load_tasks()


def load_tasks():
    for row in tree.get_children():
        tree.delete(row)

    tasks = get_tasks()
    course_tasks = {}
    for task in tasks:
        course = task[1]
        task_type = task[2]
        if course not in course_tasks:
            course_tasks[course] = {}
        if task_type not in course_tasks[course]:
            course_tasks[course][task_type] = []
        course_tasks[course][task_type].append(task)

    for course, task_types in course_tasks.items():
        course_node = tree.insert("", tk.END, text = course, open = True)
        for task_type in ['laboratory work', 'practical work', 'individual work']:  # Specify the desired order
            if task_type in task_types:
                tasks = task_types[task_type]
                task_type_node = tree.insert(course_node, tk.END, text = task_type, open = True)
                for task in tasks:
                    if task_type == 'laboratory work':
                        task_values = (f"Lab {task[3]}", task[4], task[5], task[6], task[7])
                    elif task_type == 'practical work':
                        task_values = (f"Practical {task[3]}", task[4], task[5], task[6], task[7])
                    else:
                        task_values = (task[2], task[4], task[5], task[6], task[7])  # Properly align the values
                    tree.insert(task_type_node, tk.END, values = task_values)

    root.update_idletasks()  # Force GUI update to adjust column widths


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


def on_task_type_change(event):
    task_type = task_type_combobox.get()
    if task_type == 'laboratory work' or task_type == 'practical work':
        number_label.pack(pady = 5)
        number_entry.pack(pady = 5)
    else:
        number_label.pack_forget()
        number_entry.pack_forget()


def create_gui():
    root = tk.Tk()
    root.title("University Task Manager")
    root.geometry("800x600")
    root.resizable(True, True)

    # Configure grid layout for root
    root.grid_columnconfigure(0, weight = 0)  # Fixed size for the left frame
    root.grid_columnconfigure(1, weight = 1)  # Resizable center frame
    root.grid_rowconfigure(0, weight = 1)

    # Frames
    left_frame = tk.Frame(root, width = 200, bg = 'lightgrey')
    center_frame = tk.Frame(root)
    left_frame.grid(row = 0, column = 0, sticky = "ns")
    center_frame.grid(row = 0, column = 1, sticky = "nsew")

    # Prevent the left frame from resizing
    left_frame.grid_propagate(False)

    # Configure grid layout for center frame
    center_frame.grid_rowconfigure(0, weight = 1)
    center_frame.grid_columnconfigure(0, weight = 1)

    # Left frame widgets for adding a new task
    global course_entry, task_type_combobox, deadline_entry, number_label, number_entry, tree
    tk.Label(left_frame, text = "Course").pack(pady = 5)
    course_entry = tk.Entry(left_frame)
    course_entry.pack(pady = 5)

    tk.Label(left_frame, text = "Task Type").pack(pady = 5)
    task_type_combobox = ttk.Combobox(left_frame, values = ['laboratory work', 'practical work', 'individual work'])
    task_type_combobox.pack(pady = 5)
    task_type_combobox.bind("<<ComboboxSelected>>", on_task_type_change)

    number_label = tk.Label(left_frame, text = "Number")
    number_entry = tk.Entry(left_frame)

    tk.Label(left_frame, text = "Deadline (YYYY-MM-DD)").pack(pady = 5)
    deadline_entry = tk.Entry(left_frame)
    deadline_entry.pack(pady = 5)

    tk.Button(left_frame, text = "Add Task", command = on_add_task).pack(pady = 20)
    tk.Button(left_frame, text = "Login and pull tasks from ELSE", command = on_pull_tasks).pack(pady = 20)
    tk.Button(left_frame, text = "Save the database to Dropbox", command = save_to_dropbox).pack(pady = 20)
    tk.Button(left_frame, text = "Download the database from Dropbox", command = download_from_dropbox).pack(pady = 20)

    # Center frame for displaying tasks
    columns = ("task", "stage1_status", "stage2_status", "stage3_status", "deadline")
    tree = ttk.Treeview(center_frame, columns = columns, show = 'tree headings')
    for col in columns:
        tree.heading(col, text = col)
    tree.grid(row = 0, column = 0, sticky = "nsew")

    # Add a scrollbar to the Treeview
    scrollbar = ttk.Scrollbar(center_frame, orient = tk.VERTICAL, command = tree.yview)
    tree.configure(yscroll = scrollbar.set)
    scrollbar.grid(row = 0, column = 1, sticky = 'ns')

    load_tasks()
    root.mainloop()


# Only run the GUI if this file is executed directly (not imported)
if __name__ == "__main__":
    create_table()  # Ensure the table is created
    create_gui()
