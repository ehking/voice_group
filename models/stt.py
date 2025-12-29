from typing import List, Dict


def transcribe_segments(audio_path, diarized_segments: List[Dict]) -> List[Dict]:
    # Placeholder transcription
    transcripts = []
    example_texts = ["سلام بچه‌ها امروز درباره برنامه‌هامون حرف می‌زنیم.", "کجا بریم بعد از کار؟"]
    for idx, seg in enumerate(diarized_segments):
        text = example_texts[idx % len(example_texts)]
        transcripts.append({**seg, "text": text})
    return transcripts


def normalize_persian(text: str) -> str:
    return text.replace("ي", "ی").replace("ك", "ک")
