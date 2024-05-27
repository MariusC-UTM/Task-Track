import tkinter as tk
from tkinter import ttk
from database import add_task, get_tasks, create_table
from scraper import import_tasks
import dropbox
import os

# Dropbox API key
DROPBOX_ACCESS_TOKEN = 'uat.AE_ATYgfbrbuIi6_bJh0CSjV-HXYzRYXs7xHx9S-sCrxIAfY5Yruezrw5HLzs38B8WFzQFiOLt-R5uuCKaezUxk-_sNrZlOSom-e5UHowgYFDfXXI4pa33k-lD1Q0_4TRkEij-chlgmtqZwz2_kM2D0ojnZn54eJlReMf0Kv3SneV0seziQtn8a1G11XNPp_LC1FSLA__viYxmyt5DkENU0X9heAh4FkoXZojjmADDxnVEE-IDXDm9L_yFzzkAeoQ1Wwl3b6GYFOPSttPe2vEWQBNrpI5X-b9Kf1FoqTiUuZEjsBRGau5T8wj5jhcE3zy655fvX74cgQMCmIE9FHHDrqkUpFi-8UmhDED6Rv_i7x7rAdtw8eX8kafcQz8uo6Gi0kzEAnr2f17FoZRZw7Uhk6eH1i-hp2NSMSoEQApVaHVEK0mTK2tM09UgUaao3sMKepKwAwjIeaOYuNDOQENjYwfSqQj0rlV7GPf_6dRRjPx4vUQ_wQA_B4PPZm1w7DgYuoq6mVwBtInqf7z3jUvi-fnDxCZMynY7sn5gx4LGuVd0VZV5GkWgjat3wUdtqJEtGz6KGvEdPas4Yu5He_X7ePDKfzIOtuvnSHx3Tsj7eEpkqPb3uUKmjxFQjcaUOsqAn03rxBbM_F7RhcHD8qGqsVQ2JRRAdAL4swHycAwhcZMNNRuqV7kCf7kE4tTHmCB2-5XzlOD1EVd_leeESDP1XpbA1CbxLy7Hlxch6hEa2l2RZVGU1ju8B6-1FkAoEtU0rsjmB-h3HS48oXBqcveHFtU_QS-8Il0Y8Hoo-g0j1zi5JFKAND5XSmiG3FD01e0Jldl1fAuZbcZHU6J_hKPhP0aDldV2q0DULlfj4Pxn6o2TvsPDuDSZnzEa6xJH4G6kY1AsdxQB0RqpRmLlDAQRyOwox5t4QN2sJk9Y4Uk250TjEDtoPAVg3OE0j-hOglCXKq204U8hWx-7dZUZg7pUA0v5vDjA1x8qf31vpWdM8U6BhKPCNrMzSinVCs1c58OPBMrZ6N0d2xLrCYJI_Sjn9WIaySrYwJ1UrJ_VaGFj9LI1X9-JUNRxL9ARC7OObIzgZkbB1a659NxB5tUYHaxnGLoBSm5JVaDk0htDGqNooViYf8ISZeZkS8Bou7r97j4j63SOn0Unap0W6JSu9I3yV85jK33S4Yr6H1ZA8kXjtiUVOfqT280_IpSWjY0lrh8vyefRI_y2ixUtm41QGGNjhz4v9XP0ywROYChShUSwiNKT2Kba9cJ4gZLAWuLyMZwC7-9f_ENt11f6MTxDoIYflkYYhvsQKskPnwhC1FoudwVdBUhBSEjEvAHRLbHbnYvo8TgEbBL3eSoMZ2xB7StBXO8LJU7pqcPcqkfbtyd9gEZRRXbltZsMCpsyiMiJzOhm4nnfnbTj0Dsntba_LCFEIyfHPX1Hw6qVC8k8t2sVyjkw'


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
    root.resizable(True, True)

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

    tk.Label(left_frame, text = "Deadline (Day, Month, Year)").pack(pady = 5)
    deadline_entry = tk.Entry(left_frame)
    deadline_entry.pack(pady = 5)

    tk.Button(left_frame, text = "Add Task", command = on_add_task).pack(pady = 20)

    tk.Button(left_frame, text = "Authenticate and pull tasks from ELSE", command = on_pull_tasks).pack(pady = 20)

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
