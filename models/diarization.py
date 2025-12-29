from typing import List, Dict


def heuristic_diarization(vad_segments: List[tuple], max_speakers: int = 4) -> List[Dict]:
    speakers = [f"S{i+1}" for i in range(max_speakers)]
    diarized = []
    for idx, (start, end) in enumerate(vad_segments):
        diarized.append(
            {
                "speaker": speakers[idx % len(speakers)],
                "start_ms": start,
                "end_ms": end,
                "confidence": 0.5,
            }
        )
    return diarized
