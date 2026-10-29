# Setup for terminal-capable agents

The stable integration interface is a local Python CLI. Point each agent at the repository's `SKILL.md`. These are examples, not automatic credential access.

1. **Codex CLI:** place the skill folder in Codex's supported skills directory; invoke `python scripts/video_editor.py doctor` from its root. Alternatively include the absolute path to `SKILL.md` in a prompt.
2. **Claude Code:** include the instructions as a skill or link them from project instructions. Use the same Python commands.
3. **Gemini CLI:** reference `SKILL.md` in project agent guidance (e.g. `GEMINI.md`) and authorize terminal tools as appropriate.
4. **DeepSeek / other providers:** choose a coding-agent host with a shell. The model API alone cannot edit files.
5. **ChatGPT browser:** use a connected execution environment, such as a local coding agent, rather than expecting a browser conversation to read local drives.

Optional MCP server (requires the third-party `mcp` Python package):

```sh
python -m pip install 'mcp>=1.10,<2'
python scripts/mcp_server.py
```

Configure an MCP-compatible agent to launch that Python command using its **absolute** interpreter and script paths. Prefer a dedicated virtual environment. The MCP server only exposes read-only `video_info` and `plan_trim` (dry-run) in this version. It does not directly modify files, intentionally limiting risk from arbitrary model prompts.
