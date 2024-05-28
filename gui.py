import tkinter as tk
from tkinter import ttk
from database import add_task, get_tasks, update_task, create_table
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

    # Sort courses alphabetically
    sorted_courses = sorted(course_tasks.items())

    for course, task_types in sorted_courses:
        course_node = tree.insert("", tk.END, text=course, open=True)
        for task_type in ['laboratory work', 'practical work', 'individual work']:  # Specify the desired order
            if task_type in task_types:
                tasks = task_types[task_type]

                # Sort tasks by the 'number' field for 'laboratory work' and 'practical work'
                if task_type in ['laboratory work', 'practical work']:
                    tasks.sort(key=lambda x: int(x[3]))

                task_type_node = tree.insert(course_node, tk.END, text=task_type, open=True)
                for task in tasks:
                    if task_type == 'laboratory work':
                        task_values = (f"Laboratory {task[3]}", task[4], task[5], task[6], task[7])
                    elif task_type == 'practical work':
                        task_values = (f"Practical {task[3]}", task[4], task[5], task[6], task[7])
                    else:
                        task_values = (task[2], task[4], task[5], task[6], task[7])  # Properly align the values
                    tree.insert(task_type_node, tk.END, values=task_values)


def on_pull_tasks():
    import_tasks()
    load_tasks()


def save_to_dropbox():
    dbx = dropbox.Dropbox(DROPBOX_ACCESS_TOKEN)
    with open('tasks.db', 'rb') as f:
        dbx.files_upload(f.read(), '/tasks.db', mode=dropbox.files.WriteMode.overwrite)
    print("Database saved to Dropbox")


def download_from_dropbox():
    dbx = dropbox.Dropbox(DROPBOX_ACCESS_TOKEN)
    with open('tasks.db', 'wb') as f:
        metadata, res = dbx.files_download(path='/tasks.db')
        f.write(res.content)
    print("Database downloaded from Dropbox")
    load_tasks()


def on_task_type_change(event):
    task_type = task_type_combobox.get()
    if task_type == 'laboratory work' or task_type == 'practical work':
        number_label.pack(pady=5)
        number_entry.pack(pady=5)
    else:
        number_label.pack_forget()
        number_entry.pack_forget()


def on_tree_select(event):
    selected_item = tree.selection()
    if selected_item:
        task_values = tree.item(selected_item, 'values')
        if task_values:
            task_id.set(tree.item(selected_item)['text'])
            task_entry.delete(0, tk.END)  # Clear previous text
            task_entry.insert(0, task_values[0])  # Insert new text
            performing_status_combobox.set(task_values[1])
            writing_status_combobox.set(task_values[2])
            presenting_status_combobox.set(task_values[3])
            edit_deadline_entry.delete(0, tk.END)
            edit_deadline_entry.insert(0, task_values[4])  # Insert deadline text

def on_apply_changes():
    task_id_val = task_id.get()
    task_val = task_entry.get()
    performing_status = performing_status_combobox.get()
    writing_status = writing_status_combobox.get()
    presenting_status = presenting_status_combobox.get()
    deadline_val = edit_deadline_entry.get()

    if task_id_val:
        update_task(task_id_val, task_val, performing_status, writing_status, presenting_status, deadline_val)
        load_tasks()

def on_discard_changes():
    task_id.set("")
    task_entry.set("")
    performing_status_combobox.set("")
    writing_status_combobox.set("")
    presenting_status_combobox.set("")
    edit_deadline_entry.set("")


def create_gui():
    root = tk.Tk()
    root.title("University Task Manager")
    root.geometry("800x600")
    root.resizable(True, True)

    root.grid_columnconfigure(0, weight = 0)
    root.grid_columnconfigure(1, weight = 1)
    root.grid_rowconfigure(0, weight = 1)
    root.grid_rowconfigure(1, weight = 0)

    left_frame = tk.Frame(root, width = 200, bg = 'lightgrey')
    center_frame = tk.Frame(root)
    edit_frame = tk.Frame(root, height = 100, bg = 'lightgrey')

    left_frame.grid(row = 0, column = 0, rowspan = 2, sticky = "ns")
    center_frame.grid(row = 0, column = 1, sticky = "nsew")
    edit_frame.grid(row = 1, column = 1, sticky = "ew")

    left_frame.grid_propagate(False)
    edit_frame.grid_propagate(False)

    center_frame.grid_rowconfigure(0, weight = 1)
    center_frame.grid_columnconfigure(0, weight = 1)

    global course_entry, task_type_combobox, deadline_entry, number_label, number_entry, tree
    global task_id, task_entry, performing_status_combobox, writing_status_combobox, presenting_status_combobox, edit_deadline_entry

    tk.Label(left_frame, text="Course").pack(pady=5)
    course_entry = tk.Entry(left_frame)
    course_entry.pack(pady=5)

    tk.Label(left_frame, text="Task Type").pack(pady=5)
    task_type_combobox = ttk.Combobox(left_frame, values=['laboratory work', 'practical work', 'individual work'])
    task_type_combobox.pack(pady=5)
    task_type_combobox.bind("<<ComboboxSelected>>", on_task_type_change)

    number_label = tk.Label(left_frame, text="Number")
    number_entry = tk.Entry(left_frame)

    tk.Label(left_frame, text="Deadline (YYYY-MM-DD)").pack(pady=5)
    deadline_entry = tk.Entry(left_frame)
    deadline_entry.pack(pady=5)

    tk.Button(left_frame, text="Add Task", command=on_add_task).pack(pady=20)
    tk.Button(left_frame, text="Login and pull tasks from ELSE", command=on_pull_tasks).pack(pady=20)
    tk.Button(left_frame, text="Save the database to Dropbox", command=save_to_dropbox).pack(pady=20)
    tk.Button(left_frame, text="Download the database from Dropbox", command=download_from_dropbox).pack(pady=20)

    # Center frame for displaying tasks
    columns = ("task", "performing", "writing report", "presenting report", "deadline")
    tree = ttk.Treeview(center_frame, columns=columns, show='tree headings')
    tree.heading("task", text="Task")
    tree.heading("performing", text="Performing the Task")
    tree.heading("writing report", text="Writing the Report")
    tree.heading("presenting report", text="Presenting the Report")
    tree.heading("deadline", text="Deadline")
    tree.grid(row=0, column=0, sticky="nsew")

    # Add a scrollbar to the Treeview
    scrollbar = ttk.Scrollbar(center_frame, orient=tk.VERTICAL, command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.grid(row=0, column=1, sticky='ns')

    task_id = tk.StringVar()
    task_entry = tk.Entry(edit_frame)
    performing_status_combobox = ttk.Combobox(edit_frame, values = ['not started', 'unfinished', 'finished'])
    writing_status_combobox = ttk.Combobox(edit_frame, values = ['not started', 'unfinished', 'finished'])
    presenting_status_combobox = ttk.Combobox(edit_frame, values = ['not presented', 'presented'])
    edit_deadline_entry = tk.Entry(edit_frame)

    tree.bind("<<TreeviewSelect>>", on_tree_select)

    tk.Label(edit_frame, text = "Task").grid(row = 0, column = 0, padx = 5, pady = 5)
    task_entry = tk.Entry(edit_frame)
    task_entry.grid(row = 0, column = 1, padx = 5, pady = 5)

    # Add labels and entry widgets for other task details (performing, writing report, presenting report, deadline)

    tk.Button(edit_frame, text = "Apply Changes", command = on_apply_changes).grid(row = 0, column = 6, padx = 5, pady = 5)
    tk.Button(edit_frame, text = "Discard Changes", command = on_discard_changes).grid(row = 1, column = 6, padx = 5, pady = 5)

    load_tasks()
    root.mainloop()


# Only run the GUI if this file is executed directly (not imported)
if __name__ == "__main__":
    create_table()  # Ensure the table is created
    create_gui()
