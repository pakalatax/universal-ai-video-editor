# Universal AI Video Editor

An original, **local-first AI-assisted video editing toolkit**, designed for terminal-capable agents. No cloned editor code or third-party skill files are bundled.

## Current capabilities

- Inspect media streams with FFprobe
- Trim footage; vertical and square presets; picture-in-picture
- Loudness normalization, spectral noise filtering, speed control, fades, thumbnails, clip joining
- Burn existing SRT captions
- **Beginner preset CLI**: YouTube, Shorts, square and archive output, with plan-before-render
- **Speech pause editor**: detect and compress long quiet gaps while retaining breathing space
- **Provider gateway**: text requests via OpenAI, Anthropic, Gemini, Ollama and OpenAI-compatible APIs
- **MCP adapter**: read-only media inspection, trim planning, provider-type listing
- Automated smoke tests and a Windows/macOS/Linux GitHub Actions workflow

**Not yet implemented:** automatic transcription, semantic filler/retake removal, subtitle generation, AI B-roll, speaker tracking, full GUI, semantic prompt-to-timeline generation and live authenticated multi-provider validation.

## Install locally with Git

Prerequisites: Git, Python 3, FFmpeg and FFprobe on PATH.

### Windows PowerShell

```powershell
git clone https://github.com/pakalatax/universal-ai-video-editor.git
cd universal-ai-video-editor
python scripts/video_editor.py doctor
python scripts/easy_editor.py presets
python scripts/provider_gateway.py list
```

### First video

```powershell
python scripts/easy_editor.py plan --input "E:\VideoProjects\Input\sample.mp4" --output "E:\VideoProjects\Output\sample-edited.mp4" --preset youtube
```

Review the plan and output path; then replace `plan` with `render`. The output folder must exist and the output filename must not exist.

### Speech pause cleanup

```powershell
python scripts/speech_editor.py analyze --input "recording.mp4"
python scripts/speech_editor.py render --input "recording.mp4" --output "cleaned.mp4"
```

The second command previews intended cuts; append `--approve` to render. Audio silence is not equivalent to meaningless speech: review before approval.

## AI models

Use `python scripts/provider_gateway.py list` for supported adapters. API credentials are read from environment variables; never commit them. Use `check` for a local configuration preview. Real `ask` calls require a reachable model endpoint, valid model ID, and may incur provider charges. For Ollama, start its local server and supply your installed model name.

See [provider setup](references/provider-setup.md) and [agent setup](references/agent-setup.md).

## Optional MCP plugin

Install the MCP Python package in a dedicated virtual environment:

```powershell
python -m pip install "mcp>=1.10,<2"
python scripts/mcp_server.py
```

Configure a compatible host to launch the second command with **absolute paths**. It currently exposes safe planning tools; MCP rendering is not enabled.

## Test

```powershell
python -m unittest discover -s scripts -p "test_*.py" -v
```

The latest local suite passed **12 tests** using FFmpeg 6 on Linux. CI targets Windows, macOS and Linux, but results must be inspected before claiming cross-platform completion.

Read [SKILL.md](SKILL.md), [beginner guide](references/beginner-workflows.md), [speech workflow](references/speech-workflows.md), and [advanced commands](references/advanced-workflows.md).

## Security and license

Source media is not overwritten. Outputs are new filenames; cloud text provider use is optional and subject to provider fees/privacy terms. No video uploads occur in the built-in CLI. MIT covers original repository code only; third-party models, media, codecs and services retain separate rights.

## Benchmark integrity

Do not claim to outperform commercial editors without independent, reproducible task-level comparisons. Record input fixtures, hardware, OS, FFmpeg version, quality criteria, memory use and elapsed time.
