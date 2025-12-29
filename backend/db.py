from datetime import datetime
from sqlalchemy import create_engine, Column, String, Integer, DateTime, Float, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from .config import DB_PATH

engine = create_engine(f"sqlite:///{DB_PATH}", connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()

class Job(Base):
    __tablename__ = "jobs"
    id = Column(String, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    status = Column(String, default="queued")
    progress = Column(Integer, default=0)
    input_path = Column(String)
    input_original_name = Column(String)
    duration_sec = Column(Float, default=0.0)
    settings_json = Column(Text)
    result_dir = Column(String)
    error_message = Column(Text)

class Segment(Base):
    __tablename__ = "segments"
    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(String, index=True)
    speaker = Column(String)
    start_ms = Column(Integer)
    end_ms = Column(Integer)
    text = Column(Text)
    emotion = Column(String)
    emotion_score = Column(Float)
    confidence = Column(Float)

class Event(Base):
    __tablename__ = "events"
    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(String, index=True)
    type = Column(String)
    payload_json = Column(Text)


def init_db():
    Base.metadata.create_all(bind=engine)


def get_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
