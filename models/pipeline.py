import json
from pathlib import Path
from typing import Dict

from backend.utils import write_json
from backend.config import RESULTS_DIR
from .preprocess import convert_to_wav, simple_vad
from .diarization import heuristic_diarization
from .stt import transcribe_segments, normalize_persian
from .emotion import estimate_emotion
from .analytics import build_analytics
from .summary import summarize


def run_pipeline(job_id: str, input_path: Path, settings: Dict):
    result_dir = RESULTS_DIR / job_id
    result_dir.mkdir(parents=True, exist_ok=True)
    wav_path = convert_to_wav(input_path, result_dir)
    vad_segments = simple_vad(wav_path)
    diarized = heuristic_diarization(vad_segments, max_speakers=settings.get("max_speakers", 4))
    transcripts = transcribe_segments(wav_path, diarized)
    for seg in transcripts:
        seg["text"] = normalize_persian(seg["text"])
    enriched = estimate_emotion(transcripts)
    analytics = build_analytics(enriched)
    summary = summarize(enriched)

    write_json(result_dir / "transcript.json", enriched)
    write_json(result_dir / "analytics.json", analytics)
    write_json(result_dir / "summary.json", summary)
    diar_json = [{"speaker": s["speaker"], "start": s["start_ms"], "end": s["end_ms"], "confidence": s["confidence"]} for s in diarized]
    write_json(result_dir / "diarization.json", diar_json)

    # html report
    report_path = result_dir / "report.html"
    report_html = "<html><body dir='rtl'><h1>گزارش دورهمی</h1><ul>" + "".join(
        [f"<li>{seg['speaker']} ({seg['emotion']}): {seg['text']}</li>" for seg in enriched]
    ) + "</ul></body></html>"
    report_path.write_text(report_html, encoding="utf-8")

    # build zip
    import zipfile

    zip_path = result_dir / "artifacts.zip"
    with zipfile.ZipFile(zip_path, "w") as zf:
        for item in ["transcript.json", "analytics.json", "summary.json", "diarization.json", "report.html"]:
            zf.write(result_dir / item, arcname=item)
    return enriched, analytics, summary
