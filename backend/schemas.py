from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime

class JobSettings(BaseModel):
    file_type: str
    noise_level: str
    max_speakers: int = Field(ge=2, le=10)
    interruption_sensitivity: str

class JobCreateResponse(BaseModel):
    job_id: str

class SegmentOut(BaseModel):
    speaker: str
    start_ms: int
    end_ms: int
    text: str
    emotion: str
    emotion_score: float
    confidence: float

class Analytics(BaseModel):
    talk_time: List[dict]
    interruptions: List[dict]
    turn_stats: dict
    interaction_graph: List[dict]

class SummaryOut(BaseModel):
    bullets: List[str]
    highlights: List[str]

class JobDetail(BaseModel):
    id: str
    status: str
    progress: int
    created_at: datetime
    updated_at: datetime
    settings: JobSettings
    segments: List[SegmentOut]
    analytics: Analytics
    summary: SummaryOut
    artifacts: List[str]
    error_message: Optional[str]

class ArtifactList(BaseModel):
    artifacts: List[str]
