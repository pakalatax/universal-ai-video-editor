---
name: universal-video-editor
description: Model-neutral local video editing skill for inspecting, trimming, resizing, subtitling, normalizing audio and creating picture-in-picture YouTube videos with FFmpeg. Use from Codex, Claude Code, Gemini CLI, DeepSeek-powered coding agents or any terminal-capable assistant.
---

# Universal Video Editor

Use a portable Python + FFmpeg engine, independent of any model API. Browser-only AI chats may read these instructions and plan edits but cannot edit local files without terminal access. Never claim universal native installation.

## Workflow

1. Run `python scripts/video_editor.py doctor` to check Python, FFmpeg and ffprobe.
2. Probe source with `python scripts/video_editor.py probe --input FILE`; preserve originals.
3. Draft a timestamped edit plan; confirm language, length, aspect ratio, and graphics style before substantial creative edits.
4. Review external graphics/music licenses. Do not upload media or use paid APIs without consent.
5. Run rendering commands with `--dry-run` first. All outputs must be new filenames in an existing directory.
6. Review frames, audio joins, spoken meaning and subtitle timing; verify final streams with `probe`.

## Local commands

```sh
python scripts/video_editor.py doctor
python scripts/video_editor.py probe --input input.mp4
python scripts/video_editor.py trim --input input.mp4 --output cut.mp4 --start 5 --duration 30 --dry-run
python scripts/video_editor.py normalize --input input.mp4 --output balanced.mp4
python scripts/video_editor.py vertical --input input.mp4 --output short.mp4
python scripts/video_editor.py captions --input input.mp4 --subtitles text.srt --output subtitled.mp4
python scripts/video_editor.py pip --input input.mp4 --overlay broll.mp4 --output combined.mp4
```

Every rendering command accepts `--dry-run` and refuses overwriting files. The captions command needs an existing verified SRT. The tool does not bundle transcription, AI generation, stock footage, licensing, or cloud services. Optional plugins such as Kinocut may add functions but require independent review.

Read [compatibility.md](references/compatibility.md) for differences among AI hosts and hardware limitations.
