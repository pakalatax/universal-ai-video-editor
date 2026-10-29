---
name: shot-list-from-video
description: Create a timecoded shot inventory and contact-sheet plan from video using ffprobe and FFmpeg; use for footage review, content planning, or finding B-roll opportunities.
---

# Shot list from video

1. Inspect duration, frame rate and orientation with `python scripts/video_editor.py probe --input FILE`.
2. For a short first pass, extract a frame every 5 seconds to a new empty review directory with `ffmpeg -i INPUT -vf "fps=1/5,scale=480:-2" -vsync vfr frame-%04d.jpg`. Run the command from the destination directory; never write into the source directory.
3. Use the frames to write a list of `start | end | visual content | editorial purpose | confidence`. Frame sampling cannot prove action between sampled frames.
4. Check timestamps against the audio or transcript before suggesting a cut.
5. Label unknown content as unknown. Do not invent location, identity, or events.
6. Provide a proposed, reversible B-roll plan. Only use B-roll with verified usage rights.

The skill creates a review plan, not automatic object recognition or licensed stock footage.
