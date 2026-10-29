---
name: caption-and-review
description: Add reviewed SRT subtitles to video and verify legibility, accuracy, and alignment. Use for English, Telugu or Hindi educational videos after a transcript is checked.
---

# Caption and Review

1. Obtain a verified SRT with timestamped speech, or use the experimental `scripts/auto_caption.py` only when that optional module is available and tested. Never invent spoken wording.
2. Confirm SRT numbering, time ordering, language, and fonts. Telugu/Hindi text requires a font with adequate script coverage.
3. Preview with `python scripts/video_editor.py captions --input INPUT.mp4 --subtitles VERIFIED.srt --output NEW-CAPTIONED.mp4 --dry-run`.
4. Render only after approval, omitting `--dry-run`. Existing outputs are not overwritten.
5. Examine frames near the beginning, middle and end of each caption; check safe margins, face obstruction, line length and correct speech timing.
6. The current basic renderer has default subtitle styling and burns text into video. A passing render does not imply accurate word alignment, automatic translation or animated captions.

No external prompt or skill code was copied. All text and templates here are original.
