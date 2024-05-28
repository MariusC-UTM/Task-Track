import sys
print('sys path:\n',sys.path)

from gui import create_gui
from scraper import import_tasks
from database import create_table

def main():
    create_table()
    create_gui()

if __name__ == "__main__":
    main()
