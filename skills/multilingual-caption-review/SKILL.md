---
---
name: multilingual-caption-review
description: Review English, Telugu, Hindi, and mixed-language video subtitles for timing, spelling, script and readability; use after transcription before publishing.
---

# Multilingual caption review

1. Identify the real spoken language(s) by listening, not from the requested `--language` parameter. Forced language values are not independently detected.
2. Use the optional `scripts/auto_caption.py` only on branches where that script exists; run its dry-run first and confirm `--approve` options with `--help`.
3. Check every language switch. Do not translate speech unless explicitly asked; preserve speakers' words. Mark uncertain proper nouns for manual review.
4. For Telugu, use Telugu script; for Hindi, use Devanagari; for English, use Latin script, unless the user specifies romanization.
5. Review subtitle overlap with faces and platform UI, then shorten long lines and adjust timecodes without changing meaning.
6. Export a corrected SRT and a *new* rendered video. Validate duration and inspect frames at subtitle changes.

Mixed-language recognition is an experimental capability until tested on labeled recordings. Do not report the supplied language parameter as a confidence score.
