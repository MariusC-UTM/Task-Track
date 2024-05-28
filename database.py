import sqlite3

def create_table():
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    course TEXT,
                    task_type TEXT,
                    number TEXT,
                    stage1_status TEXT DEFAULT 'not started',
                    stage2_status TEXT DEFAULT 'not started',
                    stage3_status TEXT DEFAULT 'not started',
                    deadline TEXT
                 )''')
    conn.commit()
    conn.close()

def add_task(course, task_type, deadline, number=None):
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    if task_type == 'laboratory work' or task_type == 'practical work':
        c.execute('INSERT INTO tasks (course, task_type, number, deadline) VALUES (?, ?, ?, ?)',
                  (course, task_type, number, deadline))
    else:
        c.execute('INSERT INTO tasks (course, task_type, deadline) VALUES (?, ?, ?)',
                  (course, task_type, deadline))
    conn.commit()
    conn.close()

def get_tasks():
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute('SELECT * FROM tasks')
    tasks = c.fetchall()
    conn.close()
    return tasks

def update_task(task_id, task, performing_status, writing_status, presenting_status, deadline):
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute('''UPDATE tasks SET task=?, stage1_status=?, stage2_status=?, stage3_status=?, deadline=? WHERE id=?''',
              (task, performing_status, writing_status, presenting_status, deadline, task_id))
    conn.commit()
    conn.close()
