import os
import shutil
import tkinter as tk
from tkinter import filedialog
import typer

app = typer.Typer()

@app.command()
def run():
    # Determine the project root relative to this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(script_dir, '..', '..'))
    dest_dir = os.path.join(project_root, 'services', 'retrieval', 'Datasets')
    os.makedirs(dest_dir, exist_ok=True)

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