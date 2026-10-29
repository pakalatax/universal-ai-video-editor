---
name: thumbnail-and-title
description: Generate candidate title text and extract source-video thumbnail frames for accessible YouTube publishing; use for thumbnail planning and chapter title cards.
---

# Thumbnail and title

1. Probe footage, identify video topic from a verified transcript, and ask for intended audience/language.
2. Suggest three factual titles in the user's requested language. Avoid unsupported statistics, sensational false claims or implied endorsements.
3. Select a frame at a verified timestamp using `python scripts/video_editor.py thumbnail --input INPUT --output NEW_PNG --time SECONDS`. Confirm the actual CLI flag with `--help` before running.
4. Review legibility on mobile, subject visibility, and whether caption text is cropped. Do not infer click-through rate from visual taste.
5. Add any third-party fonts/photos/logos only after licensing review. Preserve the original frame and source media.
6. Deliver the thumbnail and a concise manual review checklist.

This workflow extracts source frames; it does not implement an AI background replacement or CTR optimizer.
