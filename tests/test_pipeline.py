from pathlib import Path

from models.pipeline import run_pipeline


def test_pipeline_shapes(tmp_path):
    fake_audio = tmp_path / "audio.wav"
    fake_audio.write_bytes(b"fake")
    segments, analytics, summary = run_pipeline("test", fake_audio, {"max_speakers": 2})
    assert len(segments) >= 1
    assert "talk_time" in analytics
    assert "bullets" in summary
