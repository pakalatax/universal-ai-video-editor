#!/usr/bin/env python3
"""Beginner-oriented, offline edit planner and renderer with safe presets."""
import argparse
import json
import math
import shutil
import subprocess
import sys
from pathlib import Path

PRESETS = {
    "youtube": {"size": "1280:720", "fit": "pad", "audio": True, "description": "16:9 educational or talking-head video"},
    "short": {"size": "720:1280", "fit": "crop", "audio": True, "description": "9:16 vertical short"},
    "square": {"size": "720:720", "fit": "crop", "audio": True, "description": "1:1 social clip"},
    "archive": {"size": None, "fit": None, "audio": False, "description": "preserve original framing"},
}

def parse():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("action", choices=["presets", "plan", "render"])
    p.add_argument("--input")
    p.add_argument("--output")
    p.add_argument("--preset", choices=PRESETS, default="youtube")
    p.add_argument("--start", type=float, default=0)
    p.add_argument("--duration", type=float)
    p.add_argument("--quality", choices=["draft", "standard", "high"], default="standard")
    return p.parse_args()

def build(a):
    if not shutil.which("ffmpeg") or not shutil.which("ffprobe"):
        raise ValueError("Install FFmpeg and FFprobe on PATH")
    if not a.input or not a.output:
        raise ValueError("Supply --input and --output")
    source = Path(a.input).expanduser().resolve()
    target = Path(a.output).expanduser().resolve()
    if not source.is_file():
        raise ValueError("Input not found")
    if source == target or target.exists() or not target.parent.is_dir():
        raise ValueError("Output must be a new file in an existing directory")
    if a.start < 0 or not math.isfinite(a.start) or (a.duration is not None and (a.duration <= 0 or not math.isfinite(a.duration))):
        raise ValueError("Invalid trim timing")
    preset = PRESETS[a.preset]
    filters = []
    if preset["size"]:
        w, h = preset["size"].split(":")
        if preset["fit"] == "pad":
            filters += [f"scale={w}:{h}:force_original_aspect_ratio=decrease", f"pad={w}:{h}:(ow-iw)/2:(oh-ih)/2"]
        else:
            filters += [f"scale={w}:{h}:force_original_aspect_ratio=increase", f"crop={w}:{h}"]
        filters += ["setsar=1"]
    command = ["ffmpeg", "-hide_banner", "-n"]
    if a.start:
        command += ["-ss", str(a.start)]
    command += ["-i", str(source)]
    if a.duration:
        command += ["-t", str(a.duration)]
    command += ["-map", "0:v:0", "-map", "0:a:0?", "-sn"]
    if filters:
        command += ["-vf", ",".join(filters)]
    crf = {"draft": "28", "standard": "22", "high": "18"}[a.quality]
    command += ["-c:v", "libx264", "-preset", "veryfast", "-crf", crf]
    if preset["audio"]:
        command += ["-af", "loudnorm=I=-16:TP=-1.5:LRA=11"]
    command += ["-c:a", "aac", "-movflags", "+faststart", str(target)]
    return command

def main():
    a = parse()
    if a.action == "presets":
        print(json.dumps(PRESETS, indent=2))
        return
    command = build(a)
    print(json.dumps({"mode": a.action, "preset": a.preset, "command": command}, indent=2))
    if a.action == "render":
        subprocess.run(command, check=True)

if __name__ == "__main__":
    try:
        main()
    except (ValueError, subprocess.CalledProcessError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        sys.exit(1)
