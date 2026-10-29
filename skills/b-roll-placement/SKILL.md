---
name: b-roll-placement
description: Plan and safely insert user-owned or license-verified B-roll over narration; use for illustrated explainers, talking-head videos, and picture-in-picture segments.
---

# B-roll placement

1. Get the narration transcript and a timestamped list of claims. Do not imply visuals prove a claim they merely illustrate.
2. For each candidate shot, record source file, license/ownership, timestamp, intended start/end, aspect ratio, and relevance.
3. Probe both files. Check camera rotation and HDR-to-SDR conversion, and decide whether B-roll should cover the presenter or be picture-in-picture.
4. Preview a simple picture-in-picture with `python scripts/video_editor.py pip --input TALKING_HEAD --overlay BROLL --output NEW_OUTPUT --dry-run`.
5. Run the command only after reviewing timing and getting approval. If the built-in PIP command cannot meet an exact timed placement, stop and request a timeline-capable implementation; do not fake timing.
6. Verify voice intelligibility, visual framing, rights and final duration.

Never download arbitrary search images or use copyrighted clips merely because they are publicly visible.
