from gui import create_gui
from scraper import import_tasks
from database import create_table

def main():
    create_table()
    # import_tasks()  # Optional: Import tasks at the start
    create_gui()

if __name__ == "__main__":
    main()
