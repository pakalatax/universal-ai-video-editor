# Speech-first editing (M1)

Use `scripts/speech_editor.py` to detect and **compress long silent gaps**, preserving a configurable natural pause. It uses FFmpeg `silencedetect`, requires one audio and video stream, and does not require any AI cloud API.

1. Inspect a source without changing it:

   `python scripts/speech_editor.py analyze --input recording.mp4`

2. Preview the exact keep ranges and FFmpeg command:

   `python scripts/speech_editor.py render --input recording.mp4 --output cleaned.mp4`

3. After reviewing the ranges, explicitly approve rendering:

   `python scripts/speech_editor.py render --input recording.mp4 --output cleaned.mp4 --approve`

Default: compress silences lasting at least 0.8 seconds to 0.3 seconds. Use `--minimum-pause` and `--retain` to tune. The algorithm is not speech-semantic: soft-spoken words, room tone, music and silence thresholds can cause false cuts. Always review the content and avoid running it on multitrack music projects without manual inspection.

**Not included yet:** ASR, word-level transcript editing, filler identification, retake selection, Telugu-language validation or captions. These require separate tested model adapters and word-alignment benchmarks.
