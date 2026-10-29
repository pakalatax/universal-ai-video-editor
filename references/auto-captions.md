# Optional offline auto-captions (experimental)

This is a first-party wrapper around Faster-Whisper and FFmpeg. It does not clone another editor. The speech-recognition model remains an external dependency with its own licenses and accuracy limitations.

## Install on Windows PowerShell

Use Python 3.11 in an isolated environment:

```powershell
py -3.11 -m venv .venv-transcribe
& ".\\.venv-transcribe\\Scripts\\python.exe" -m pip install "faster-whisper==1.2.1"
$env:HF_HOME = "E:\\VideoProjects\\Models"
```

Model cache can be moved to any existing folder. Initial model download needs internet; media is processed locally. Model files must not be committed.

## Preview first

```powershell
& ".\\.venv-transcribe\\Scripts\\python.exe" scripts/auto_caption.py --input "E:\\VideoProjects\\Input\\clip.mp4" --output "E:\\VideoProjects\\Output\\clip-captioned.mp4" --language auto
```

No model download or output writing occurs during the preview.

## Run after confirming the plan

```powershell
& ".\\.venv-transcribe\\Scripts\\python.exe" scripts/auto_caption.py --input "E:\\VideoProjects\\Input\\clip.mp4" --output "E:\\VideoProjects\\Output\\clip-captioned.mp4" --language auto --approve
```

Languages: `auto`, `telugu`, `hindi`, `english`. For code switching, `auto` enables per-segment multilingual detection; accuracy is unverified for Telugu/Hindi/mixed speech. Default model is `base` on CPU with int8 quantization and four threads. For better accuracy on stronger machines, test `--model small` separately.

The program creates a burned-in MP4 and an editable SRT. It refuses existing output files, requires audio and video streams, uses 48 kHz AAC output, and never uploads the source. It does **not** remove fillers, translate subtitles, correct grammar, generate visuals, or guarantee word timing. Review outputs carefully before publishing.

## Tests

```powershell
python -m unittest discover -s scripts -p "test_*.py" -v
```

The first milestone contains unit tests and dry-run validation. A successful Windows ASR + render acceptance test on real input is required before release.
