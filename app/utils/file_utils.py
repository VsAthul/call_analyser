import uuid
from pathlib import Path
from fastapi import UploadFile
import shutil
from app.core.logger import logger

def save_uploaded_file(file: UploadFile, upload_folder: str) -> str:
    extension = Path(file.filename).suffix
    filename = f"{uuid.uuid4()}{extension}"
    file_path = Path(upload_folder) / filename
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)  # proper stream copy
        return str(file_path)
    except Exception:
        logger.exception(
            f"Failed to save uploaded file: {file.filename}"
        )
        raise