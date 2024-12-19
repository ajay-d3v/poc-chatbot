import os
import shutil
from modules.store import create_db

def clear_folder(folder_path):
    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)  # Deletes the folder and all its contents
        os.makedirs(folder_path)   # Recreates an empty folder

def process_uploaded_files(files):
    uploads_folder = os.path.join("data/uploads")
    db_folder = os.path.join("db")
    
    # Clear previous data
    clear_folder(uploads_folder)
    clear_folder(db_folder)
    
    # Save all uploaded files
    for file in files:
        file_path = os.path.join(uploads_folder, file.name)
        with open(file_path, "wb") as f:
            f.write(file.getbuffer())

    # Process and create a single database from all files
    create_db(uploads_folder)
