import json
import uuid
from pathlib import Path
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, Request
from fastapi.responses import FileResponse, HTMLResponse
from sqlalchemy.orm import Session

from .templates import templates
from .db import Job, Segment, Event, get_session
from .schemas import JobCreateResponse, JobSettings, JobDetail, SegmentOut, Analytics, SummaryOut, ArtifactList
from .config import RESULTS_DIR, MAX_UPLOAD_MB
from .utils import allowed_file, save_upload, list_artifacts

router = APIRouter()


@router.post("/api/jobs", response_model=JobCreateResponse)
async def create_job(
    file: UploadFile = File(...),
    file_type: str = Form("جلسه خودمونی"),
    noise_level: str = Form("متوسط"),
    max_speakers: int = Form(4),
    interruption_sensitivity: str = Form("med"),
    db: Session = Depends(get_session),
):
    if not allowed_file(file.filename):
        raise HTTPException(status_code=400, detail="فرمت فایل پشتیبانی نمی‌شود")
    size = 0
    if file.size:
        size = file.size
    if size and size > MAX_UPLOAD_MB * 1024 * 1024:
        raise HTTPException(status_code=400, detail="حجم فایل زیاد است")

    job_id = str(uuid.uuid4())
    path = save_upload(file, job_id)
    settings = JobSettings(
        file_type=file_type,
        noise_level=noise_level,
        max_speakers=max_speakers,
        interruption_sensitivity=interruption_sensitivity,
    )
    job = Job(
        id=job_id,
        status="queued",
        progress=0,
        input_path=str(path),
        input_original_name=file.filename,
        settings_json=settings.json(ensure_ascii=False),
        result_dir=str(RESULTS_DIR / job_id),
    )
    db.add(job)
    db.commit()
    return JobCreateResponse(job_id=job_id)


@router.get("/api/jobs")
def list_jobs(db: Session = Depends(get_session)):
    jobs = db.query(Job).order_by(Job.created_at.desc()).all()
    response = []
    for job in jobs:
        response.append(
            {
                "id": job.id,
                "status": job.status,
                "progress": job.progress,
                "created_at": job.created_at,
                "updated_at": job.updated_at,
                "file_name": job.input_original_name,
            }
        )
    return response


def assemble_job_detail(job: Job, db: Session) -> JobDetail:
    segments = db.query(Segment).filter(Segment.job_id == job.id).all()
    seg_out = [
        SegmentOut(
            speaker=s.speaker,
            start_ms=s.start_ms,
            end_ms=s.end_ms,
            text=s.text,
            emotion=s.emotion,
            emotion_score=s.emotion_score,
            confidence=s.confidence,
        )
        for s in segments
    ]
    analytics_path = Path(job.result_dir) / "analytics.json"
    summary_path = Path(job.result_dir) / "summary.json"
    analytics = Analytics(**json.loads(analytics_path.read_text(encoding="utf-8"))) if analytics_path.exists() else Analytics(talk_time=[], interruptions=[], turn_stats={}, interaction_graph=[])
    summary = SummaryOut(**json.loads(summary_path.read_text(encoding="utf-8"))) if summary_path.exists() else SummaryOut(bullets=[], highlights=[])
    settings = JobSettings(**json.loads(job.settings_json))
    return JobDetail(
        id=job.id,
        status=job.status,
        progress=job.progress,
        created_at=job.created_at,
        updated_at=job.updated_at,
        settings=settings,
        segments=seg_out,
        analytics=analytics,
        summary=summary,
        artifacts=list_artifacts(Path(job.result_dir)),
        error_message=job.error_message,
    )


@router.get("/api/jobs/{job_id}", response_model=JobDetail)
def job_detail(job_id: str, db: Session = Depends(get_session)):
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="یافت نشد")
    return assemble_job_detail(job, db)


@router.get("/api/jobs/{job_id}/artifacts", response_model=ArtifactList)
def job_artifacts(job_id: str, db: Session = Depends(get_session)):
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="یافت نشد")
    artifacts = list_artifacts(Path(job.result_dir))
    return ArtifactList(artifacts=artifacts)


@router.get("/api/jobs/{job_id}/download")
def download_zip(job_id: str):
    zip_path = Path(RESULTS_DIR) / job_id / "artifacts.zip"
    if not zip_path.exists():
        raise HTTPException(status_code=404, detail="آماده نیست")
    return FileResponse(zip_path, filename=f"{job_id}.zip")


@router.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})


@router.get("/jobs/{job_id}", response_class=HTMLResponse)
async def job_view(job_id: str, request: Request):
    return templates.TemplateResponse("job_detail.html", {"request": request, "job_id": job_id})
