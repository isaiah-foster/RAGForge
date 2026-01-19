import os
import shutil
import tkinter as tk
from tkinter import filedialog
from .cli import app
from core.paths import DATA_BASE_PATH, DATASET_PATH

@app.command()
def add_docs():
    """
    Add raw documents from local files to the embed queue
    """
    #determine datasets path
    dest_dir = DATASET_PATH
    dest_dir.mkdir(parents=True, exist_ok=True)

    # Hide the main tkinter window
    root = tk.Tk()
    root.withdraw()

    # Open file selection dialog
    file_paths = filedialog.askopenfilenames(title="Select files to upload")
    if not file_paths:
        print("No files selected. Exiting.")
        return

    for file_path in file_paths:
        try:
            filename = os.path.basename(file_path)
            dest_path = os.path.join(dest_dir, filename)
            shutil.copy2(file_path, dest_path)
            print(f"Copied '{filename}' to '{dest_dir}'")
        except Exception as e:
            print(f"Failed to copy '{file_path}': {e}")