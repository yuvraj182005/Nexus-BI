import hashlib
from pathlib import Path

from fastapi import UploadFile


class LocalObjectStorage:
    def __init__(self, root: str) -> None:
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)

    async def save_upload(self, key: str, upload: UploadFile) -> tuple[int, str]:
        destination = self.root / key
        destination.parent.mkdir(parents=True, exist_ok=True)
        digest = hashlib.sha256()
        size = 0
        with destination.open("wb") as file_handle:
            while chunk := await upload.read(1024 * 1024):
                file_handle.write(chunk)
                digest.update(chunk)
                size += len(chunk)
        await upload.close()
        return size, digest.hexdigest()

    def path_for(self, key: str) -> Path:
        path = (self.root / key).resolve()
        if self.root.resolve() not in path.parents:
            raise ValueError("Invalid storage key")
        return path

    def delete(self, key: str) -> None:
        path = self.path_for(key)
        if path.exists():
            path.unlink()
