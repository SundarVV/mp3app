import sys
import os
from PySide6.QtCore import QFile
from PySide6.QtUiTools import QUiLoader


def resource_path(relative_path):
    """ Get the absolute path to resource, works for PyInstaller and local dev. """
    try:
        base_path = sys._MEIPASS  # For PyInstaller bundle
    except AttributeError:
        base_path = os.path.abspath(".")  # For normal Python execution
    return os.path.join(base_path, relative_path)


def load_main_window():
    # Define the path to the .ui file using the resource_path function
    ui_file_path = resource_path("path_to_MP3App.ui")

    # Ensure the .ui file exists
    ui_file = QFile(ui_file_path)
    if not ui_file.exists():
        print(f"Error: UI file not found at {ui_file_path}")
        sys.exit(-1)

    # Open the .ui file and load it
    ui_file.open(QFile.ReadOnly)
    loader = QUiLoader()
    ui = loader.load(ui_file)
    ui_file.close()
