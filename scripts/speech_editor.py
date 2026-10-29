#!/usr/bin/env python3
"""Detect and compress long silences in narrated videos without cloud services."""
import argparse
import json
import math
import re
import shutil
import subprocess
import sys
from pathlib import Path

START = re.compile(r"silence_start:\s*([0-9.]+)")
END = re.compile(r"silence_end:\s*([0-9.]+)")

def intervals(log, total):
    """Parse FFmpeg silencedetect intervals, including a trailing silence."""
    result, pending = [], None
    for line in log.splitlines():
        s, e = START.search(line), END.search(line)
        if s:
            pending = float(s.group(1))
        if e and pending is not None:
            end = float(e.group(1))
            if 0 <= pending < end <= total + 0.1:
                result.append((pending, min(end, total)))
            pending = None
    if pending is not None and pending < total:
        result.append((pending, total))
    return result

def keep_ranges(total, silences, threshold=0.8, retain=0.3):
    """Retain short silences and a natural pause centered in each long silence."""
    if not 0 <= retain < threshold or threshold <= 0:
        raise ValueError("Require 0 <= retain < threshold")
    removed = []
    for start, end in silences:
        if end - start >= threshold:
            excess = end - start - retain
            removed.append((start + retain / 2, end - retain / 2))
            if excess <= 0:
                removed.pop()
    kept, cursor = [], 0.0
    for start, end in removed:
        if start > cursor:
            kept.append((cursor, start))
        cursor = max(cursor, end)
    if cursor < total:
        kept.append((cursor, total))
    return [(round(a, 6), round(b, 6)) for a, b in kept if b - a > 0.01]

def probe_duration(source):
    raw = subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=nw=1:nk=1", str(source)], text=True).strip()
    value = float(raw)
    if not math.isfinite(value) or value <= 0:
        raise ValueError("Source has invalid duration")
    return value

def analyze(source, total, threshold, db):
    cmd = ["ffmpeg", "-hide_banner", "-nostats", "-i", str(source), "-vn", "-af", f"silencedetect=noise={db}dB:d={threshold}", "-f", "null", "-"]
    proc = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, text=True)
    if proc.returncode:
        raise ValueError("FFmpeg silence analysis failed")
    return intervals(proc.stderr, total)

def render(source, output, kept, dry):
    if not kept:
        raise ValueError("No media would remain")
    # Require one video and one audio stream; do not guess missing stream treatment.
    graph = []
    for i, (a, b) in enumerate(kept):
        graph += [f"[0:v]trim=start={a}:end={b},setpts=PTS-STARTPTS[v{i}]", f"[0:a:0]atrim=start={a}:end={b},asetpts=PTS-STARTPTS[a{i}]"]
    graph.append("".join(f"[v{i}][a{i}]" for i in range(len(kept))) + f"concat=n={len(kept)}:v=1:a=1[v][a]")
    cmd = ["ffmpeg", "-hide_banner", "-n", "-i", str(source), "-filter_complex", ";".join(graph), "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-preset", "veryfast", "-crf", "22", "-c:a", "aac", str(output)]
    if dry:
        print(json.dumps({"dry_run": True, "argv": cmd}, indent=2))
    else:
        subprocess.run(cmd, check=True)

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("action", choices=["analyze", "render"])
    p.add_argument("--input", required=True)
    p.add_argument("--output")
    p.add_argument("--minimum-pause", type=float, default=0.8)
    p.add_argument("--retain", type=float, default=0.3)
    p.add_argument("--noise-db", type=float, default=-35)
    p.add_argument("--approve", action="store_true", help="Explicit approval to render")
    a = p.parse_args()
    if not shutil.which("ffmpeg") or not shutil.which("ffprobe"):
        raise ValueError("FFmpeg and FFprobe required")
    src = Path(a.input).expanduser().resolve()
    if not src.is_file():
        raise ValueError("Input not found")
    if not -90 <= a.noise_db <= -5 or not 0 <= a.retain < a.minimum_pause:
        raise ValueError("Invalid silence settings")
    duration = probe_duration(src)
    silence = analyze(src, duration, a.minimum_pause, a.noise_db)
    kept = keep_ranges(duration, silence, a.minimum_pause, a.retain)
    report = {"input": str(src), "original_seconds": duration, "silences": silence, "keep_ranges": kept, "expected_seconds": round(sum(b - x for x, b in kept), 3)}
    print(json.dumps(report, indent=2))
    if a.action == "render":
        if not a.output:
            raise ValueError("--output required")
        out = Path(a.output).expanduser().resolve()
        if out.exists() or out == src or not out.parent.is_dir():
            raise ValueError("Output must be a new file in an existing directory")
        render(src, out, kept, dry=not a.approve)

if __name__ == "__main__":
    try:
        main()
    except (ValueError, subprocess.CalledProcessError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        sys.exit(1)
