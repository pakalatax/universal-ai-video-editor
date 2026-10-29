#!/usr/bin/env python3
"""Additional offline FFmpeg operations: no overwrites, no network services."""
import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path


def source_file(name):
    path = Path(name).expanduser().resolve()
    if not path.is_file():
        raise ValueError(f"Input file not found: {path}")
    return path


def output_file(name, inputs):
    path = Path(name).expanduser().resolve()
    if path in inputs or path.exists() or not path.parent.is_dir():
        raise ValueError("Use a new output path in an existing directory, separate from inputs")
    return path


def run(args, dry):
    if dry:
        print(json.dumps({"dry_run": True, "argv": [str(a) for a in args]}, indent=2))
    else:
        subprocess.run([str(a) for a in args], check=True)


def command(args):
    if not shutil.which("ffmpeg"):
        raise ValueError("FFmpeg is required on PATH")
    media = source_file(args.input)
    other = source_file(args.second) if args.action == "join" else None
    sources = {media} | ({other} if other else set())
    dest = output_file(args.output, sources)
    ff = ["ffmpeg", "-hide_banner", "-n", "-i", media]
    if args.action == "speed":
        if not 0.5 <= args.factor <= 2.0:
            raise ValueError("Speed must be between 0.5 and 2.0")
        ff += ["-filter_complex", f"[0:v]setpts=PTS/{args.factor}[v];[0:a]atempo={args.factor}[a]", "-map", "[v]", "-map", "[a]"]
    elif args.action == "fade":
        if args.duration <= 0:
            raise ValueError("Fade duration must be positive")
        ff += ["-vf", f"fade=t=in:st=0:d={args.duration}"]
    elif args.action == "denoise":
        ff += ["-af", "afftdn=nf=-25"]
    elif args.action == "thumbnail":
        if args.time < 0:
            raise ValueError("Timestamp must be nonnegative")
        ff += ["-ss", str(args.time), "-frames:v", "1", "-update", "1", dest]
        run(ff, args.dry_run)
        return
    elif args.action == "join":
        ff += ["-i", other, "-filter_complex", "[0:v]setpts=PTS-STARTPTS,scale=1280:720,setsar=1[v0];[1:v]setpts=PTS-STARTPTS,scale=1280:720,setsar=1[v1];[0:a]aresample=async=1:first_pts=0[a0];[1:a]aresample=async=1:first_pts=0[a1];[v0][a0][v1][a1]concat=n=2:v=1:a=1[v][a]", "-map", "[v]", "-map", "[a]"]
    if args.action in ("speed", "join"):
        ff += ["-c:v", "libx264", "-preset", "veryfast", "-crf", "22", "-c:a", "aac", dest]
    elif args.action in ("fade", "denoise"):
        ff += ["-c:v", "libx264" if args.action == "fade" else "copy", "-preset", "veryfast", "-c:a", "aac", dest]
    run(ff, args.dry_run)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    subs = parser.add_subparsers(dest="action", required=True)
    for action in ("speed", "fade", "denoise", "thumbnail", "join"):
        p = subs.add_parser(action)
        p.add_argument("--input", required=True)
        p.add_argument("--output", required=True)
        p.add_argument("--dry-run", action="store_true")
        if action == "speed":
            p.add_argument("--factor", type=float, required=True)
        if action == "fade":
            p.add_argument("--duration", type=float, default=0.5)
        if action == "thumbnail":
            p.add_argument("--time", type=float, required=True)
        if action == "join":
            p.add_argument("--second", required=True)
    command(parser.parse_args())


if __name__ == "__main__":
    try:
        main()
    except (ValueError, subprocess.CalledProcessError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        sys.exit(1)
