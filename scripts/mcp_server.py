#!/usr/bin/env python3
"""Minimal read-only MCP adapter, optional dependency: mcp>=1.10,<2."""
import json
import shutil
import subprocess
from pathlib import Path

try:
    from mcp.server.fastmcp import FastMCP
except ImportError as exc:
    raise SystemExit("Install optional dependency: python -m pip install 'mcp>=1.10,<2'") from exc

mcp = FastMCP("universal-video-editor")

@mcp.tool()
def video_info(path: str) -> dict:
    """Read codec, duration and streams from an existing local video."""
    p = Path(path).expanduser().resolve()
    if not p.is_file() or not shutil.which("ffprobe"):
        raise ValueError("Readable input and FFprobe are required")
    raw = subprocess.check_output(["ffprobe", "-v", "error", "-show_format", "-show_streams", "-of", "json", str(p)], text=True)
    return json.loads(raw)

@mcp.tool()
def plan_trim(path: str, output: str, start: float, duration: float) -> dict:
    """Return a safe proposed FFmpeg trim command without executing it."""
    p = Path(path).expanduser().resolve()
    out = Path(output).expanduser().resolve()
    if not p.is_file() or out.exists() or p == out or not out.parent.is_dir():
        raise ValueError("Input must exist and output must be a new path")
    if start < 0 or duration <= 0:
        raise ValueError("Invalid time range")
    return {"dry_run": True, "argv": ["ffmpeg", "-hide_banner", "-n", "-ss", str(start), "-i", str(p), "-t", str(duration), "-c:v", "libx264", "-preset", "veryfast", "-crf", "22", "-c:a", "aac", str(out)]}

if __name__ == "__main__":
    mcp.run(transport="stdio")
