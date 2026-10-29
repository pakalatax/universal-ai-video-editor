"""Optional local ASR to short-caption video workflow.

Requires faster-whisper for approved rendering; preview mode is dependency-free.
"""

import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys


LANGUAGES = {"auto": None, "telugu": "te", "hindi": "hi", "english": "en"}


def srt_time(seconds):
    total = max(0, round(seconds * 1000))
    hours, total = divmod(total, 3600000)
    minutes, total = divmod(total, 60000)
    sec, millis = divmod(total, 1000)
    return f"{hours:02d}:{minutes:02d}:{sec:02d},{millis:03d}"


def group_words(words, max_words=5, max_duration=3.2, max_chars=38):
    """Generate non-overlapping captions using model word timestamps."""
    groups, current = [], []
    for raw in words:
        word = {"start": float(raw.start), "end": float(raw.end), "text": raw.word.strip()}
        if not word["text"] or word["end"] <= word["start"]:
            continue
        if current and (len(current) >= max_words
                        or word["end"] - current[0]["start"] > max_duration
                        or sum(len(w["text"]) + 1 for w in current) + len(word["text"]) > max_chars
                        or word["start"] - current[-1]["end"] > 0.7):
            groups.append(current)
            current = []
        current.append(word)
    if current:
        groups.append(current)
    return [(group[0]["start"], group[-1]["end"], " ".join(w["text"] for w in group))
            for group in groups]


def make_srt(groups):
    return "".join(f"{i}\n{srt_time(start)} --> {srt_time(end)}\n{text}\n\n"
                   for i, (start, end, text) in enumerate(groups, 1))


def probe_media(path):
    ffprobe = shutil.which("ffprobe")
    if not ffprobe:
        raise RuntimeError("ffprobe is required on PATH")
    result = subprocess.run([ffprobe, "-v", "error", "-show_entries",
                             "stream=codec_type", "-of", "json", str(path)],
                            capture_output=True, text=True, check=True)
    streams = json.loads(result.stdout)["streams"]
    if not any(s["codec_type"] == "video" for s in streams) or not any(
            s["codec_type"] == "audio" for s in streams):
        raise ValueError("Input must contain both video and audio")


def main(argv=None):
    parser = argparse.ArgumentParser(description="Local AI transcription + short caption rendering")
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--language", choices=LANGUAGES, default="auto")
    parser.add_argument("--model", default="base")
    parser.add_argument("--cpu-threads", type=int, default=4)
    parser.add_argument("--approve", action="store_true", help="Run ASR and render; omit for plan only")
    args = parser.parse_args(argv)

    source, output = args.input.resolve(), args.output.resolve()
    if not source.is_file():
        parser.error(f"Input does not exist: {source}")
    if source.suffix.lower() not in {".mp4", ".mov", ".mkv", ".webm"}:
        parser.error("Input must be a video file")
    if output.suffix.lower() != ".mp4":
        parser.error("Output must be .mp4")
    if not output.parent.is_dir():
        parser.error("Output directory does not exist")
    if output.exists() or source == output:
        parser.error("Output already exists or would overwrite input")
    if args.cpu_threads < 1 or args.cpu_threads > 32:
        parser.error("cpu-threads must be between 1 and 32")
    srt_path = output.with_suffix(".srt")
    if srt_path.exists():
        parser.error(f"Subtitle output exists: {srt_path}")
    if not shutil.which("ffmpeg") or not shutil.which("ffprobe"):
        parser.error("FFmpeg and ffprobe must be installed")
    probe_media(source)

    if not args.approve:
        print(json.dumps({"dry_run": True, "input": str(source), "output": str(output),
                          "subtitles": str(srt_path), "language": args.language,
                          "model": args.model, "requires": "faster-whisper", "uploads": False}, indent=2))
        return 0

    try:
        from faster_whisper import WhisperModel
    except ImportError as exc:
        parser.error(f"Install faster-whisper in the active Python environment: {exc}")

    model = WhisperModel(args.model, device="cpu", compute_type="int8", cpu_threads=args.cpu_threads)
    segments, info = model.transcribe(str(source), language=LANGUAGES[args.language],
                                      beam_size=3, word_timestamps=True,
                                      multilingual=(args.language == "auto"))
    words = [word for segment in segments for word in (segment.words or [])]
    groups = group_words(words)
    if not groups:
        raise RuntimeError("No recognizable speech found; no files written")

    # Use a relative SRT path from the output directory to avoid Windows drive-colon escaping.
    # Stage subtitles in a temporary filename until rendering succeeds.
    import tempfile
    with tempfile.TemporaryDirectory(prefix="auto-captions-") as tmp:
        staged = Path(tmp) / "captions.srt"
        staged.write_text(make_srt(groups), encoding="utf-8")
        # FFmpeg parses the absolute subtitle path as a filter expression.
        filter_path = str(staged).replace("\\", "/").replace(":", "\\:").replace("'", "\\'")
        ffmpeg_args = ["ffmpeg", "-hide_banner", "-n", "-i", str(source),
                       "-vf", f"subtitles='{filter_path}':force_style='FontName=Arial,FontSize=11,Outline=2,MarginV=85,Alignment=2'",
                       "-c:v", "libx264", "-preset", "veryfast", "-crf", "20",
                       "-c:a", "aac", "-ar", "48000", "-b:a", "192k", str(output)]
        subprocess.run(ffmpeg_args, check=True)
        srt_path.write_text(make_srt(groups), encoding="utf-8")
    print(json.dumps({"rendered": str(output), "subtitles": str(srt_path),
                      "detected_language": info.language, "language_confidence": info.language_probability,
                      "captions": len(groups)}, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
