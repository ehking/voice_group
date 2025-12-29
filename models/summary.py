from typing import List, Dict


def summarize(segments: List[Dict]):
    bullets = []
    highlights = []
    for seg in segments:
        bullets.append(f"{seg['speaker']} در زمان {seg['start_ms']/1000:.1f}s گفت: {seg['text']}")
        if seg.get("emotion") and seg["emotion"] != "خنثی":
            highlights.append(f"لحظه احساسی ({seg['emotion']}): {seg['text']}")
    return {"bullets": bullets[:5], "highlights": highlights[:3]}
