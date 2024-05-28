import tkinter as tk
from tkinter import ttk
from database import add_task, get_tasks, update_task, create_table, get_task_by_id
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
        task_id = task[0]
        course = task[1]
        task_type = task[2]
        if course not in course_tasks:
            course_tasks[course] = {}
        if task_type not in course_tasks[course]:
            course_tasks[course][task_type] = []
        course_tasks[course][task_type].append((task_id, task))

    # Sort courses alphabetically
    sorted_courses = sorted(course_tasks.items())

    for course, task_types in sorted_courses:
        course_node = tree.insert("", tk.END, text=course, open=True, tags=('course',))
        for task_type in ['laboratory work', 'practical work', 'individual work']:  # Specify the desired order
            if task_type in task_types:
                tasks = task_types[task_type]

                # Sort tasks by the 'number' field for 'laboratory work' and 'practical work'
                if task_type in ['laboratory work', 'practical work']:
                    tasks.sort(key=lambda x: int(x[1][3]))

                task_type_node = tree.insert(course_node, tk.END, text=task_type, open=True, tags=('task_type',))
                for task_id, task_values in tasks:
                    if task_type == 'laboratory work':
                        task_values_with_id = (f"Laboratory {task_values[3]}", task_values[4], task_values[5], task_values[6], task_values[7])
                    elif task_type == 'practical work':
                        task_values_with_id = (f"Practical {task_values[3]}", task_values[4], task_values[5], task_values[6], task_values[7])
                    else:
                        task_values_with_id = (task_values[2], task_values[4], task_values[5], task_values[6], task_values[7])  # Properly align the values
                    # print(task_values[0], task_values[1], task_values[2], task_values_with_id)
                    tree.insert(task_type_node, tk.END, text=task_id, values=task_values_with_id, tags=('task',))


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
        item_tags = tree.item(selected_item, 'tags')
        if 'course' in item_tags:
            task_id_val = tree.item(selected_item, 'text')
            print('course:', task_id_val)
        elif 'task_type' in item_tags:
            task_id_val = tree.item(selected_item, 'text')
            print('task_type:', task_id_val)
        elif 'task' in item_tags:
            task_values = tree.item(selected_item, 'values')
            if task_values:
                task_id.set(tree.item(selected_item)['text'])  # The ID of the task
                print('task id:', task_id.get())
                course_name.set(tree.item(tree.parent(tree.parent(selected_item)))['text'])
                task_type.set(tree.item(tree.parent(selected_item))['text'])
                task_entry.delete(0, tk.END)
                task_entry.insert(0, task_values[0])
                performing_status_combobox.set(task_values[1])
                writing_status_combobox.set(task_values[2])
                presenting_status_combobox.set(task_values[3])
                edit_deadline_entry.delete(0, tk.END)
                edit_deadline_entry.insert(0, task_values[4])


def on_apply_changes():
    print('applying changes')
    selected_item = tree.selection()
    if selected_item:
        item_tags = tree.item(selected_item, 'tags')
        if 'course' in item_tags:
            task_id_val = tree.item(selected_item, 'text')
            print('course:', task_id_val)
        elif 'task_type' in item_tags:
            task_id_val = tree.item(selected_item, 'text')
            print('task_type:', task_id_val)
        elif 'task' in item_tags:
            task_id_val = tree.item(selected_item, 'text')
            # or
            # task_id_val = task_id.get()
            # print('task id:', task_id_val)
            task_val = task_entry.get()
            performing_status = performing_status_combobox.get()
            writing_status = writing_status_combobox.get()
            presenting_status = presenting_status_combobox.get()
            deadline_val = edit_deadline_entry.get()

            print('applying data: ', task_id_val, task_val, performing_status, writing_status, presenting_status, deadline_val)
            if task_id_val:
                update_task(task_id_val, task_val, performing_status, writing_status, presenting_status, deadline_val)
                load_tasks()
            else:
                print('can\'t apply data')


def on_discard_changes():
    task_id.set("")
    task_entry.delete(0, tk.END)
    performing_status_combobox.set("")
    writing_status_combobox.set("")
    presenting_status_combobox.set("")
    edit_deadline_entry.delete(0, tk.END)


def create_vertical_left_bar(left_frame):
    global course_entry, task_type_combobox, deadline_entry, number_label, number_entry

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


def create_horizontal_bottom_bar(edit_frame):
    global task_entry, performing_status_combobox, writing_status_combobox, presenting_status_combobox, edit_deadline_entry, task_id, course_name, task_type

    course_name = tk.StringVar()
    task_type = tk.StringVar()
    task_id = tk.StringVar()

    tk.Label(edit_frame, text="Course:").grid(row=0, column=0, padx=5, pady=5, sticky='w')
    tk.Label(edit_frame, textvariable=course_name).grid(row=0, column=1, padx=5, pady=5, sticky='w')

    tk.Label(edit_frame, text="Task Type:").grid(row=1, column=0, padx=5, pady=5, sticky='w')
    tk.Label(edit_frame, textvariable=task_type).grid(row=1, column=1, padx=5, pady=5, sticky='w')

    tk.Label(edit_frame, text="Task ID:").grid(row=2, column=0, padx=5, pady=5, sticky='w')
    tk.Label(edit_frame, textvariable=task_id).grid(row=2, column=1, padx=5, pady=5, sticky='w')

    tk.Label(edit_frame, text="Task").grid(row=0, column=3, padx=5, pady=5)
    task_entry = tk.Entry(edit_frame)
    task_entry.grid(row=0, column=4, padx=5, pady=5)

    tk.Label(edit_frame, text="Performing the Task").grid(row=0, column=5, padx=5, pady=5)
    performing_status_combobox = ttk.Combobox(edit_frame, values=['not started', 'unfinished', 'finished'])
    performing_status_combobox.grid(row=0, column=6, padx=5, pady=5)

    tk.Label(edit_frame, text="Writing the Report").grid(row=1, column=3, padx=5, pady=5)
    writing_status_combobox = ttk.Combobox(edit_frame, values=['not started', 'unfinished', 'finished'])
    writing_status_combobox.grid(row=1, column=4, padx=5, pady=5)

    tk.Label(edit_frame, text="Presenting the Report").grid(row=1, column=5, padx=5, pady=5)
    presenting_status_combobox = ttk.Combobox(edit_frame, values=['not presented', 'presented'])
    presenting_status_combobox.grid(row=1, column=6, padx=5, pady=5)

    tk.Label(edit_frame, text="Deadline").grid(row=2, column=3, padx=5, pady=5)
    edit_deadline_entry = tk.Entry(edit_frame)
    edit_deadline_entry.grid(row=2, column=4, padx=5, pady=5)

    tk.Button(edit_frame, text="Apply Changes", command=on_apply_changes).grid(row=0, column=7, padx=5, pady=5)
    tk.Button(edit_frame, text="Discard Changes", command=on_discard_changes).grid(row=1, column=7, padx=5, pady=5)


def create_central_box(center_frame):
    global tree

    columns = ("task", "performing", "writing report", "presenting report", "deadline")
    tree = ttk.Treeview(center_frame, columns=columns, show='tree headings')
    tree.heading("task", text="Task")
    tree.heading("performing", text="Performing the Task")
    tree.heading("writing report", text="Writing the Report")
    tree.heading("presenting report", text="Presenting the Report")
    tree.heading("deadline", text="Deadline")
    tree.grid(row=0, column=0, sticky="nsew")

    scrollbar = ttk.Scrollbar(center_frame, orient=tk.VERTICAL, command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.grid(row=0, column=1, sticky='ns')

    tree.bind("<<TreeviewSelect>>", on_tree_select)


def create_gui():
    root = tk.Tk()
    root.title("University Task Manager")
    root.geometry("1050x600")
    root.resizable(True, True)

    root.grid_columnconfigure(0, weight=0)
    root.grid_columnconfigure(1, weight=1)
    root.grid_rowconfigure(0, weight=1)
    root.grid_rowconfigure(1, weight=0)

    left_frame = tk.Frame(root, width=200, bg='lightgrey')
    center_frame = tk.Frame(root)
    edit_frame = tk.Frame(root, height=100, bg='lightgrey')

    left_frame.grid(row=0, column=0, rowspan=2, sticky="ns")
    center_frame.grid(row=0, column=1, sticky="nsew")
    edit_frame.grid(row=1, column=1, sticky="ew")

    left_frame.grid_propagate(False)
    edit_frame.grid_propagate(False)

    center_frame.grid_rowconfigure(0, weight=1)
    center_frame.grid_columnconfigure(0, weight=1)

    create_vertical_left_bar(left_frame)
    create_central_box(center_frame)
    create_horizontal_bottom_bar(edit_frame)

    load_tasks()
    root.mainloop()


if __name__ == "__main__":
    create_table()  # Ensure the table is created
    create_gui()
