# Universal AI Video Editor

A **model-neutral, local-first** video editing skill for terminal-capable AI agents using Codex, Claude Code, Gemini CLI, DeepSeek or other language models.

## Implemented in v0.1

- Inspect audio and video streams via FFprobe
- Trim videos
- Convert to vertical 9:16
- Normalize audio loudness
- Burn verified SRT subtitles into video
- Add picture-in-picture footage
- Preview planned FFmpeg commands with `--dry-run`
- Preserve original footage and refuse overwriting outputs

**Not yet implemented:** automatic speech transcription, silence detection, AI B-roll generation, motion graphics, music generation, stock-media sourcing, and a universal MCP server. Browser-only chat products need a separate execution integration.

## Requirements

Python 3, FFmpeg and FFprobe on PATH. For all video editing functions, the FFmpeg build should include libx264 and the subtitles/libass filter.

## Get started

```bash
python scripts/video_editor.py doctor
python scripts/video_editor.py probe --input input.mp4
python scripts/video_editor.py trim --input input.mp4 --output cut.mp4 --start 5 --duration 30 --dry-run
```

Remove `--dry-run` after reviewing the command. Use a unique output filename. See [SKILL.md](SKILL.md) for all commands and [compatibility](references/compatibility.md) for host-specific limitations.

## Security

Review scripts before granting agent execution permission. Never publish footage, recordings, credentials, third-party media or model weights without the appropriate rights or authorization.

## License

MIT for the original project code and documentation. FFmpeg, codecs, models and all third-party content have separate license requirements.
