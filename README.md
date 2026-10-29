# Universal AI Video Editor

An original, **local-first video editing toolkit** for terminal-capable AI agents. The same Python + FFmpeg commands can be used by Codex, Claude Code, Gemini CLI, and coding agents powered by DeepSeek or other models.

## Implemented features

- FFprobe media inspection and stream information
- Video trimming, 9:16 conversion, picture-in-picture
- Loudness normalization and spectral noise filtering
- Existing SRT subtitle burn-in
- Video speed adjustments (0.5–2×), fade-in effects
- Image thumbnail extraction at specified timestamps
- Join two narrated clips (normalizes to 1280×720)
- No-overwrite safety, dry-run command previews
- Optional **read-only MCP server**: video information and trim planning
- Automated smoke tests and GitHub Actions workflow for Windows, macOS and Linux

**Not yet implemented:** transcription, automatic silence/filler removal, AI-generated B-roll, sophisticated motion graphics, automated clip ranking, voice isolation, or a complete GUI. No unsupported claim of superiority over other repositories is made.

## Requirements

Python 3 and FFmpeg/FFprobe on PATH. Certain features need libx264, AAC, and the libass subtitles filter. Optional MCP support requires `mcp>=1.10,<2`. The basic editor has no cloud API or per-video quota.

## Start here

```sh
python scripts/video_editor.py doctor
python scripts/video_editor.py probe --input input.mp4
python scripts/video_editor.py trim --input input.mp4 --output trimmed.mp4 --start 2 --duration 30 --dry-run
python scripts/advanced_editor.py thumbnail --input input.mp4 --output preview.jpg --time 10
python -m unittest discover -s scripts -p 'test_*.py' -v
```

See [SKILL.md](SKILL.md), [advanced workflows](references/advanced-workflows.md), [AI-host setup](references/agent-setup.md), and [compatibility](references/compatibility.md).

## Agent integration

The skill is *model-neutral*, not natively available in every AI chat application. Use a terminal-capable agent and point it to `SKILL.md`. For an MCP-capable host, configure the optional `scripts/mcp_server.py` process. In this initial adapter, MCP tools intentionally cannot execute edits.

## Security and licenses

Original footage and any existing output are protected from overwrite. Review third-party tools and media licenses before distributing them. No videos are uploaded by this project. MIT license applies to this project's original code; media and external dependencies retain their separate licenses.

## Benchmarks

GitHub Actions provides a cross-platform correctness smoke-test baseline. Render-speed and resource benchmarks should report hardware, OS, FFmpeg version, exact input assets, quality checks and repeatable methodology before making comparative claims.
