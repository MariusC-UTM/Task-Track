import requests
from bs4 import BeautifulSoup
from database import add_task


def scrape_tasks():
    url = "https://www.university-website.com/tasks"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    tasks = []
    for task in soup.find_all('div', class_ = 'task'):
        course = task.find('span', class_ = 'course').text
        task_type = task.find('span', class_ = 'task_type').text
        deadline = task.find('span', class_ = 'deadline').text
        tasks.append({'course': course, 'task_type': task_type, 'deadline': deadline})

    return tasks


def import_tasks():
    tasks = scrape_tasks()
    for task in tasks:
        add_task(task['course'], task['task_type'], task['deadline'])
