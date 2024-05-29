import sqlite3


# Implement the functionality to select the database to operate on:
# tasks_local.db, tasks_dropbox.db, tasks_else.db


def create_table():
    with sqlite3.connect("tasks.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                course TEXT NOT NULL,
                task_type TEXT NOT NULL,
                number INTEGER,
                performing_status TEXT,
                writing_status TEXT,
                presenting_status TEXT,
                deadline TEXT
            )
        """)
        conn.commit()


def add_task(course, task_type, number, deadline):
    with sqlite3.connect("tasks.db") as conn:
        cursor = conn.cursor()
        if task_type in ['laboratory work', 'practical work']:
            cursor.execute("""
                INSERT INTO tasks (course, task_type, number, deadline)
                VALUES (?, ?, ?, ?)
            """, (course, task_type, number, deadline))
        else:
            cursor.execute("""
                INSERT INTO tasks (course, task_type, deadline)
                VALUES (?, ?, ?)
            """, (course, task_type, deadline))
        conn.commit()


def get_tasks():
    with sqlite3.connect("tasks.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tasks")
        return cursor.fetchall()


def get_task_by_id(task_id):
    with sqlite3.connect("tasks.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
        return cursor.fetchone()


def update_task(task_id, course, task_type, number, performing_status, writing_status, presenting_status, deadline):
    with sqlite3.connect("tasks.db") as conn:
        cursor = conn.cursor()
        if task_type in ['laboratory work', 'practical work']:
            cursor.execute("""
                UPDATE tasks
                SET course = ?, task_type = ?, number = ?, performing_status = ?, writing_status = ?, presenting_status = ?, deadline = ?
                WHERE id = ?
            """, (course, task_type, number, performing_status, writing_status, presenting_status, deadline, task_id))
        else:
            cursor.execute("""
                UPDATE tasks
                SET course = ?, task_type = ?, performing_status = ?, writing_status = ?, presenting_status = ?, deadline = ?
                WHERE id = ?
            """, (course, task_type, performing_status, writing_status, presenting_status, deadline, task_id))
        conn.commit()


def delete_task(task_id):
    with sqlite3.connect("tasks.db") as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        conn.commit()
