import sqlite3


def create_table():
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY,
                    course TEXT NOT NULL,
                    task_type TEXT NOT NULL,
                    number INTEGER,
                    stage1_status TEXT,
                    stage2_status TEXT,
                    stage3_status TEXT,
                    deadline TEXT NOT NULL
                 )''')
    conn.commit()
    conn.close()

def add_task(course, task_type, deadline, number=None):
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute('''INSERT INTO tasks (course, task_type, number, stage1_status, stage2_status, stage3_status, deadline)
                 VALUES (?, ?, ?, 'not started', 'not started', 'not presented', ?)''',
              (course, task_type, number, deadline))
    conn.commit()
    conn.close()

def get_tasks():
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute('SELECT * FROM tasks')
    tasks = c.fetchall()
    conn.close()
    return tasks
