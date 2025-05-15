from database.db_manager import init_db
from view.ui import launch_ui

if __name__ == "__main__":
    init_db()
    launch_ui()
