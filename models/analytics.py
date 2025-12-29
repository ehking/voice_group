from typing import List, Dict
from collections import defaultdict


def build_analytics(segments: List[Dict]):
    talk = defaultdict(float)
    interruptions = []
    interaction_graph = defaultdict(lambda: defaultdict(int))
    prev_speaker = None
    for seg in segments:
        duration = (seg["end_ms"] - seg["start_ms"]) / 1000.0
        talk[seg["speaker"]] += duration
        if prev_speaker and prev_speaker != seg["speaker"]:
            interaction_graph[prev_speaker][seg["speaker"]] += 1
        prev_speaker = seg["speaker"]
    talk_time = [{"speaker": k, "seconds": v} for k, v in talk.items()]
    turn_stats = {
        "avg_turn_seconds": sum(t["seconds"] for t in talk_time) / len(segments) if segments else 0,
        "turns": len(segments),
    }
    interaction_list = []
    for a, targets in interaction_graph.items():
        for b, count in targets.items():
            interaction_list.append({"from": a, "to": b, "count": count})
    return {
        "talk_time": talk_time,
        "interruptions": interruptions,
        "turn_stats": turn_stats,
        "interaction_graph": interaction_list,
    }
