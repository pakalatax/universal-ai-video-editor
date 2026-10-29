#!/usr/bin/env python3
"""Offline, no-overwrite FFmpeg CLI for AI-agent video editing."""
import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

def file(value):
    p = Path(value).expanduser().resolve()
    if not p.is_file():
        raise ValueError(f"Missing input: {p}")
    return p

def invoke(args, dry=False):
    if dry:
        print(json.dumps({"dry_run": True, "argv": list(map(str, args))}, indent=2))
    else:
        subprocess.run(list(map(str, args)), check=True)

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    subs = parser.add_subparsers(dest="action", required=True)
    subs.add_parser("doctor")
    for kind in ("probe", "trim", "normalize", "vertical", "captions", "pip"):
        p = subs.add_parser(kind)
        p.add_argument("--input", required=True)
        if kind != "probe":
            p.add_argument("--output", required=True)
            p.add_argument("--dry-run", action="store_true")
        if kind == "trim":
            p.add_argument("--start", type=float, required=True)
            p.add_argument("--duration", type=float, required=True)
        if kind == "captions":
            p.add_argument("--subtitles", required=True)
        if kind == "pip":
            p.add_argument("--overlay", required=True)
    a = parser.parse_args()
    tools = {k: shutil.which(k) for k in ("ffmpeg", "ffprobe")}
    if a.action == "doctor":
        print(json.dumps({"python": sys.version.split()[0], "tools": tools}, indent=2))
        return 0 if all(tools.values()) else 2
    if not all(tools.values()):
        raise ValueError("ffmpeg and ffprobe required on PATH")
    src = file(a.input)
    if a.action == "probe":
        invoke(["ffprobe", "-v", "error", "-show_format", "-show_streams", "-of", "json", src])
        return 0
    inputs = {src}
    if a.action == "captions":
        sub = file(a.subtitles)
        inputs.add(sub)
    if a.action == "pip":
        overlay = file(a.overlay)
        inputs.add(overlay)
    out = Path(a.output).expanduser().resolve()
    if out in inputs or out.exists() or not out.parent.is_dir():
        raise ValueError("Output must be a new file in an existing folder, distinct from inputs")
    cmd = ["ffmpeg", "-hide_banner", "-n"]
    if a.action == "trim":
        if a.start < 0 or a.duration <= 0:
            raise ValueError("Invalid start/duration")
        cmd += ["-ss", str(a.start), "-i", src, "-t", str(a.duration), "-c:v", "libx264", "-preset", "veryfast", "-crf", "22", "-c:a", "aac", out]
    elif a.action == "normalize":
        cmd += ["-i", src, "-map", "0:v?", "-map", "0:a:0", "-c:v", "copy", "-af", "loudnorm=I=-16:TP=-1.5:LRA=11", "-c:a", "aac", out]
    elif a.action == "vertical":
        cmd += ["-i", src, "-vf", "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920", "-c:v", "libx264", "-preset", "veryfast", "-crf", "22", "-c:a", "aac", out]
    elif a.action == "captions":
        escaped = sub.as_posix().replace("\\", "\\\\").replace(":", "\\:").replace("'", "\\'")
        cmd += ["-i", src, "-vf", "subtitles='" + escaped + "'", "-c:v", "libx264", "-preset", "veryfast", "-crf", "22", "-c:a", "copy", out]
    elif a.action == "pip":
        cmd += ["-i", src, "-i", overlay, "-filter_complex", "[1:v]scale=iw/4:-2[p];[0:v][p]overlay=W-w-24:H-h-24:shortest=0[v]", "-map", "[v]", "-map", "0:a?", "-c:v", "libx264", "-preset", "veryfast", "-crf", "22", "-c:a", "copy", out]
    invoke(cmd, a.dry_run)
    return 0

if __name__ == "__main__":
    try:
        sys.exit(main())
    except (ValueError, subprocess.CalledProcessError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        sys.exit(1)
