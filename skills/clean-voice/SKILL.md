---
name: clean-voice
description: Inspect and improve speech audio in a video using offline denoising and loudness normalization. Use for talking-head education videos with uneven level or modest background noise.
---

# Clean Voice

1. Probe the source and confirm it has an audio track. Measure loudness before suggesting gain changes.
2. For modest steady noise, preview: `python scripts/advanced_editor.py denoise --input INPUT.mp4 --output NEW-DENOISED.mp4 --dry-run`.
3. For loudness leveling, preview: `python scripts/video_editor.py normalize --input INPUT.mp4 --output NEW-LEVELED.mp4 --dry-run`.
4. Render only after approval and inspect the resulting sound. The denoise filter may make speech metallic; compare with the original rather than assuming improvement.
5. The current normalization path does not explicitly lock sample rate; if distributing a YouTube export, verify it is 48 kHz and adjust the final encoding when needed.
6. Do not describe denoising as voice isolation, remove copyrighted background music automatically, or claim that audio statistics alone prove quality.

This skill uses the repository's original FFmpeg wrapper commands and includes no copied third-party skill.
