# Advanced editing commands

Use `python scripts/advanced_editor.py` with one of these operations. Supply existing source files and unique output names. All render commands support `--dry-run`.

```sh
python scripts/advanced_editor.py speed --input lesson.mp4 --output faster.mp4 --factor 1.25
python scripts/advanced_editor.py fade --input lesson.mp4 --output fade.mp4 --duration 0.6
python scripts/advanced_editor.py denoise --input lesson.mp4 --output less-noisy.mp4
python scripts/advanced_editor.py thumbnail --input lesson.mp4 --output poster.jpg --time 12
python scripts/advanced_editor.py join --input part1.mp4 --second part2.mp4 --output combined.mp4
```

Limitations: speed and join require one audio stream in each source; join normalizes video size to 1280x720 and expects compatible frame timing. `denoise` applies FFmpeg spectral noise reduction, not voice isolation. `fade` applies a fade-in only. Captions require an externally prepared SRT file. Always check the result visually and audibly; avoid resampling repeatedly.

## Reproducible evaluation

Measure feature correctness and resources on a repeatable local fixture, not self-declared quality rankings. Report codec support, failure rates, elapsed render time, peak RAM and output verification, with operating system, FFmpeg build, input resolution and hardware disclosed. Do not claim superior visual quality without independent blinded evaluations using representative footage.
