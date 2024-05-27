import sqlite3

def create_connection():
    return sqlite3.connect('tasks.db')

def create_table():
    conn = create_connection()
    with conn:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY,
            course TEXT NOT NULL,
            task_type TEXT CHECK(task_type IN ('laboratory work', 'practical work', 'individual work', 'project')),
            stage1_status TEXT CHECK(stage1_status IN ('not started', 'unfinished', 'finished')),
            stage2_status TEXT CHECK(stage2_status IN ('not started', 'unfinished', 'finished')),
            stage3_status TEXT CHECK(stage3_status IN ('not presented', 'presented')),
            deadline DATE,
            additional_info TEXT
        );
        """)
    conn.close()

def add_task(course, task_type, deadline):
    conn = create_connection()
    with conn:
        conn.execute("INSERT INTO tasks (course, task_type, stage1_status, stage2_status, stage3_status, deadline) VALUES (?, ?, 'not started', 'not started', 'not presented', ?);", (course, task_type, deadline))
    conn.close()

def get_tasks():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, course, task_type, stage1_status, stage2_status, stage3_status, deadline FROM tasks;")
    rows = cursor.fetchall()
    conn.close()
    return rows
