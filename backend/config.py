from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
STORAGE_DIR = BASE_DIR / "storage"
DB_PATH = BASE_DIR / "storage" / "database.db"
UPLOAD_DIR = STORAGE_DIR / "uploads"
RESULTS_DIR = STORAGE_DIR / "results"
LOG_DIR = STORAGE_DIR / "logs"
TMP_DIR = STORAGE_DIR / "tmp"

MAX_UPLOAD_MB = 200
ALLOWED_EXTENSIONS = {"mp3", "wav", "m4a"}

WHISPER_MODEL = "small"
CPU_ONLY = True

WORKER_POLL_INTERVAL = 2.0
WORKER_PARALLEL_JOBS = 3
