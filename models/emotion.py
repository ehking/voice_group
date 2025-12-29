from typing import List, Dict


def estimate_emotion(transcripts: List[Dict]) -> List[Dict]:
    emotions = ["شاد", "خنثی", "عصبانی", "هیجان‌زده"]
    enriched = []
    for idx, seg in enumerate(transcripts):
        label = emotions[idx % len(emotions)]
        enriched.append({**seg, "emotion": label, "emotion_score": 0.6})
    return enriched
