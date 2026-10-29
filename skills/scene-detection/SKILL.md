---
name: scene-detection
description: Analyze video shot boundaries using FFmpeg scene scores and produce a reviewable cut list; use when asked to find scene changes.
---

# Scene detection

Inspect video metadata with `python scripts/video_editor.py probe --input FILE` before edits. Run FFmpeg `select='gt(scene,0.35)',showinfo` on the input for candidate boundaries, then review nearby frames. A fixed threshold is a heuristic, not semantic understanding. Save a timestamped proposed edit list; never silently delete shots. Keep the source untouched and render only after approval. Do not claim that every scene break was found.
