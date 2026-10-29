# Provider gateway (M2)

The provider gateway accepts the same prompt across OpenAI Responses, Anthropic Messages, Gemini generateContent, Ollama chat and OpenAI-compatible chat APIs. The CLI does not require extra Python packages.

## Setup

```sh
python scripts/provider_gateway.py list
python scripts/provider_gateway.py check --provider ollama --model YOUR_LOCAL_MODEL
python scripts/provider_gateway.py ask --provider ollama --model YOUR_LOCAL_MODEL --prompt "Suggest a conservative edit plan"
```

For cloud providers, set the appropriate environment variable locally (never commit keys): `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, `GEMINI_API_KEY`, or `COMPATIBLE_API_KEY`. Specify a model ID confirmed in your provider account; do not hardcode model names into public setup instructions. Cloud calls can incur usage charges. `check` is offline and confirms configuration only, not authentication or model readiness.

OpenAI-compatible providers require an explicit `--endpoint`, for example an endpoint ending in `/v1/chat/completions`. Only HTTPS remote endpoints or HTTP loopback endpoints are allowed. Never pass user-controlled untrusted endpoints with credentials. This initial gateway supports text generation only; not images, video, tool calling, retries, cost accounting or structured constrained decoding. Validate model-generated JSON before using it to plan edits; never execute returned command text.

## Git installation (Windows PowerShell)

```powershell
git clone https://github.com/pakalatax/universal-ai-video-editor.git
cd universal-ai-video-editor
python scripts/video_editor.py doctor
python scripts/provider_gateway.py list
```

For Codex or Claude Code, reference `SKILL.md` from the agent's skills folder or workspace. Gemini CLI can load it through its local project guidance. A local MCP-capable agent can launch `scripts/mcp_server.py` after installing `mcp`. Browser ChatGPT, Claude and Gemini do not automatically acquire direct drive access by cloning a repository.
