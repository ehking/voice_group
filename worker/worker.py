import json
import time
import traceback
from pathlib import Path
from multiprocessing.pool import ThreadPool

from sqlalchemy.orm import Session

from backend.db import SessionLocal, Job, Segment
from backend.config import WORKER_POLL_INTERVAL, WORKER_PARALLEL_JOBS, LOG_DIR
from models.pipeline import run_pipeline


def process_job(job_id: str):
    db: Session = SessionLocal()
    log_path = LOG_DIR / f"{job_id}.log"
    try:
        job = db.query(Job).filter(Job.id == job_id).first()
        if not job:
            return
        job.status = "running"
        job.progress = 10
        db.commit()
        settings = json.loads(job.settings_json)
        enriched, analytics, summary = run_pipeline(job_id, Path(job.input_path), settings)
        # store segments
        db.query(Segment).filter(Segment.job_id == job_id).delete()
        for seg in enriched:
            db.add(
                Segment(
                    job_id=job_id,
                    speaker=seg["speaker"],
                    start_ms=seg["start_ms"],
                    end_ms=seg["end_ms"],
                    text=seg["text"],
                    emotion=seg.get("emotion", ""),
                    emotion_score=seg.get("emotion_score", 0.0),
                    confidence=seg.get("confidence", 0.0),
                )
            )
        job.status = "done"
        job.progress = 100
        db.commit()
    except Exception as exc:  # pylint: disable=broad-except
        db = SessionLocal()
        job = db.query(Job).filter(Job.id == job_id).first()
        if job:
            job.status = "error"
            job.error_message = str(exc)
            job.progress = 100
            db.commit()
        log_path.parent.mkdir(parents=True, exist_ok=True)
        log_path.write_text(traceback.format_exc(), encoding="utf-8")
    finally:
        db.close()


def poll_loop():
    pool = ThreadPool(WORKER_PARALLEL_JOBS)
    while True:
        db = SessionLocal()
        running = db.query(Job).filter(Job.status == "running").count()
        available = max(WORKER_PARALLEL_JOBS - running, 0)
        if available:
            jobs = (
                db.query(Job)
                .filter(Job.status.in_(["queued", "running"]))
                .order_by(Job.created_at)
                .limit(available)
                .all()
            )
            for job in jobs:
                if job.status == "queued":
                    pool.apply_async(process_job, args=(job.id,))
        db.close()
        time.sleep(WORKER_POLL_INTERVAL)


def requeue_running():
    db = SessionLocal()
    jobs = db.query(Job).filter(Job.status == "running").all()
    for job in jobs:
        job.status = "queued"
        job.progress = 0
    db.commit()
    db.close()


if __name__ == "__main__":
    requeue_running()
    poll_loop()
