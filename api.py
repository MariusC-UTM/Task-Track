from flask import Flask, request, jsonify
from database import create_connection, add_task, get_tasks, create_table

app = Flask(__name__)

@app.route('/tasks', methods=['GET'])
def get_tasks_api():
    tasks = get_tasks()
    return jsonify(tasks)

@app.route('/task', methods=['POST'])
def add_task_api():
    data = request.get_json()
    add_task(data['course'], data['task_type'], data['deadline'])
    return jsonify({"status": "success"}), 201

if __name__ == '__main__':
    create_table()
    app.run(debug=True)
