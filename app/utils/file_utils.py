import uuid
from pathlib import Path

from fastapi import UploadFile

import shutil

def save_uploaded_file(file: UploadFile, upload_folder: str) -> str:
    extension = Path(file.filename).suffix
    filename = f"{uuid.uuid4()}{extension}"
    file_path = Path(upload_folder) / filename
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)  # proper stream copy
    return str(file_path)