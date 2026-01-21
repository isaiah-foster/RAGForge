from pathlib import Path
import requests
import mimetypes
import typer
import tkinter as tk
import typer
from tkinter import filedialog
from core.config import load_server_url
from .main import app

API_URL = load_server_url()

def upload_files(api_url: str, file_paths: list[str], field_name: str = "files", timeout: int = 300) -> dict:
    handles = []
    try:
        files = []
        for fp in file_paths:
            p = Path(fp)
            if not p.is_file():
                raise FileNotFoundError(str(p))

            mime = mimetypes.guess_type(p.name)[0] or "application/octet-stream"
            fh = p.open("rb")
            handles.append(fh)

            # IMPORTANT: must match FastAPI parameter name: files
            files.append((field_name, (p.name, fh, mime)))

        r = requests.post(f"{api_url}/upload", files=files, timeout=timeout)
        r.raise_for_status()
        return r.json()
    finally:
        for fh in handles:
            try:
                fh.close()
            except Exception:
                pass
@app.command()
def upload():
    """
    Add raw documents from local files to the embed queue
    """
    root = tk.Tk()
    root.withdraw()

    file_paths = list(filedialog.askopenfilenames(title="Select files to upload"))
    if not file_paths:
        typer.echo("No files selected. Exiting.")
        return

    try:
        resp = upload_files(API_URL, file_paths)
        typer.echo(f"Uploaded {resp.get('count', 0)} file(s).")
        for p in resp.get("saved", []):
            typer.echo(p)
    except requests.exceptions.RequestException as e:
        typer.echo(f"Connection error: {e}")
    except Exception as e:
        typer.echo(f"Error: {e}")