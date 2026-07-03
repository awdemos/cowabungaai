"""CRUD Operations for the Files Bucket."""

import os
from fastapi import UploadFile
from cowabunga_api.data.database.base import DatabaseClient


class CRUDFileBucket:
    """CRUD Operations for FileBucket."""

    def __init__(self, db: DatabaseClient, model: type[UploadFile]):
        self.client: DatabaseClient = db
        self.model: type[UploadFile] = model
        self.storage_path = os.getenv("FILE_STORAGE_PATH", "/tmp/cowabunga_files")

    async def upload(self, file: UploadFile, id_: str):
        """Upload a file to the file bucket."""
        os.makedirs(self.storage_path, exist_ok=True)
        file_path = os.path.join(self.storage_path, id_)
        with open(file_path, "wb") as f:
            f.write(await file.read())
        return {"path": file_path}

    async def download(self, id_: str):
        """Get a file from the file bucket."""
        file_path = os.path.join(self.storage_path, id_)
        with open(file_path, "rb") as f:
            return f.read()

    async def delete(self, id_: str):
        """Delete a file from the file bucket."""
        file_path = os.path.join(self.storage_path, id_)
        if os.path.exists(file_path):
            os.remove(file_path)
        return True
