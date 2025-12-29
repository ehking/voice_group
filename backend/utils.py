import os
import uuid
from pathlib import Path
import shutil
import json

from fastapi import UploadFile

from .config import ALLOWED_EXTENSIONS, UPLOAD_DIR


def allowed_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def save_upload(file: UploadFile, job_id: str) -> Path:
    upload_dir = UPLOAD_DIR / job_id
    upload_dir.mkdir(parents=True, exist_ok=True)
    ext = file.filename.split(".")[-1]
    new_name = f"{uuid.uuid4().hex}.{ext}"
    dest = upload_dir / new_name
    with dest.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return dest


def write_json(path: Path, payload):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)


def format_progress(status: str, progress: int) -> dict:
    return {"status": status, "progress": progress}


def list_artifacts(result_dir: Path):
    artifacts = []
    if result_dir.exists():
        for p in sorted(result_dir.iterdir()):
            artifacts.append(p.name)
    return artifacts
