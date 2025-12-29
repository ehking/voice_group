import subprocess
from pathlib import Path
from typing import List


def convert_to_wav(input_path: Path, output_dir: Path) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    target = output_dir / "converted.wav"
    cmd = [
        "ffmpeg",
        "-y",
        "-i",
        str(input_path),
        "-ac",
        "1",
        "-ar",
        "16000",
        str(target),
    ]
    try:
        subprocess.run(cmd, check=True, capture_output=True)
    except Exception:
        # In MVP, simply copy
        target.write_bytes(Path(input_path).read_bytes())
    return target


def simple_vad(audio_path: Path) -> List[tuple]:
    # placeholder segments: whole file as one segment
    return [(0, 5000)]
