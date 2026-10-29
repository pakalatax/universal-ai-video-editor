# Editing without technical knowledge

Use `scripts/easy_editor.py` for a consistent beginner workflow. Have the assistant ask for **one input video**, **one output filename** and **one destination**: YouTube, Shorts, square social, or Archive.

1. List the four presets: `python scripts/easy_editor.py presets`.
2. Preview the exact plan before writing files:

   `python scripts/easy_editor.py plan --input recording.mp4 --output finished.mp4 --preset youtube`

3. After approval, run the corresponding `render` command.
4. Check the output visually, verify audio intelligibility and subtitle correctness if subtitles were added separately.

The “youtube” preset letterboxes as necessary to avoid cropping. Shorts and square presets **crop the center**, which can cut off a speaker at the edge. For human tracking, smart reframing, or background removal, state that a separate AI model is required. The preset does not automatically remove mistakes or generate content. For low-memory machines, choose `--quality draft` before the final `standard` or `high` render.

## Benchmark acceptance criteria

Measure against actual tasks, not marketing claims. Release gates: zero source overwrites; every output probed successfully; no missing audio without explicit intent; caption timing reviewed; repeatable test results on Windows, macOS and Linux. Speed benchmarks must use the same source, codec, resolution, encoder preset and machine. Independent, blind subjective quality tests are needed to claim visual superiority.
