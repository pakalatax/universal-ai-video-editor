---
name: audio-quality-audit
description: Measure speech loudness, clipping risk, and silent passages using local FFmpeg; use when checking voice recordings or YouTube audio quality.
---

# Audio quality audit

1. Inspect with `python scripts/video_editor.py probe --input FILE` and verify there is an audio stream.
2. Run `ffmpeg -hide_banner -i INPUT -af "loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json" -vn -f null NUL` on Windows (use `/dev/null` on Unix). This **measures** loudness, but without a two-pass workflow its analysis is not proof of output compliance.
3. To locate long silence candidates, run `ffmpeg -hide_banner -i INPUT -af "silencedetect=noise=-35dB:d=0.6" -f null NUL`. Treat results as candidates, not filler speech.
4. Explain clipping/peaks, noise, silence, and whether normalization would help. Do not remove content without review.
5. If the user approves, use the repository's `normalize` command to create a new file, then measure the result independently. Keep the original.

Do not guarantee broadcast loudness or noise-free audio without measured output and listening review.
