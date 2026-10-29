---
name: format-for-social
description: Prepare a video for vertical Shorts, horizontal YouTube, square social posts, or archive export using existing offline quality presets. Use when the user asks to resize or repurpose footage.
---

# Format for Social

1. Inspect input dimensions, rotation and HDR/SDR metadata with `python scripts/video_editor.py probe --input INPUT.mp4`.
2. Choose one existing preset: `youtube` (1280x720 padded), `short` (720x1280 cropped), `square` (720x720 cropped), or `archive` (original framing). Explain any important crop or padding.
3. Preview: `python scripts/easy_editor.py plan --input INPUT.mp4 --output NEW-VIDEO.mp4 --preset short --quality standard`.
4. After approval run the same command with `render` instead of `plan`. The output must be a new filename.
5. Check that text, faces and limbs remain visible. For portrait footage with important background elements, use manual preview before accepting a center crop.
6. For HLG/PQ HDR sources, do not assume simple resize converts HDR to SDR correctly. Use a separately verified tone-mapping workflow.

This skill reuses first-party preset code. Rendering quality and aspect ratio are not equivalent to AI face tracking.
