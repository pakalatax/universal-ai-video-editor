---
name: safe-cut
description: Inspect, trim, split by approved timestamps, or join video clips using the repository's existing offline FFmpeg commands. Use when the user wants basic cutting without replacing original footage.
---

# Safe Cut

1. Identify the exact input file, requested timestamps and output location. Ask for timestamps if unclear; never guess which spoken content to remove.
2. Verify FFmpeg with `python scripts/video_editor.py doctor` and inspect streams with `python scripts/video_editor.py probe --input INPUT.mp4`.
3. Preview the cut:

   `python scripts/video_editor.py trim --input INPUT.mp4 --output NEW-CUT.mp4 --start 5 --duration 20 --dry-run`

4. After explicit approval, repeat without `--dry-run`. Never overwrite the source or an existing destination.
5. For a two-clip join, use `python scripts/advanced_editor.py join --input A.mp4 --second B.mp4 --output NEW-JOIN.mp4 --dry-run` first. The join implementation requires audio on both clips and creates a 1280x720 result; do not use it for a portrait preservation requirement.
6. Probe the output and review the cut boundaries and spoken meaning.

This skill is an original orchestration of the repository's existing commands; no third-party skill source was copied.
