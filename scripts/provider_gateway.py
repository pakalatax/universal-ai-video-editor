#!/usr/bin/env python3
"""Model-neutral text gateway. Requires explicitly configured model IDs and credentials."""
import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

PROVIDERS = {
    "openai": {"env": "OPENAI_API_KEY", "url": "https://api.openai.com/v1/responses"},
    "anthropic": {"env": "ANTHROPIC_API_KEY", "url": "https://api.anthropic.com/v1/messages"},
    "gemini": {"env": "GEMINI_API_KEY", "url": "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"},
    "ollama": {"env": None, "url": "http://127.0.0.1:11434/api/chat"},
    "compatible": {"env": "COMPATIBLE_API_KEY", "url": None},
}

def request_for(provider, model, prompt, endpoint=None):
    if provider not in PROVIDERS or not model or not prompt.strip():
        raise ValueError("Provider, model and prompt required")
    config = PROVIDERS[provider]
    url = endpoint or config["url"]
    if not url:
        raise ValueError("Compatible providers require --endpoint")
    if provider == "gemini":
        url = url.replace("{model}", urllib.parse.quote(model, safe="-_."))
    parsed = urllib.parse.urlsplit(url)
    if parsed.scheme not in ("https", "http") or not parsed.netloc or parsed.username or parsed.password or parsed.fragment:
        raise ValueError("Invalid provider URL")
    if parsed.scheme != "https" and parsed.hostname not in ("localhost", "127.0.0.1", "::1"):
        raise ValueError("Remote provider endpoints must use HTTPS")
    key = os.environ.get(config["env"], "") if config["env"] else ""
    if config["env"] and not key:
        raise ValueError(f"Set {config['env']} in the environment")
    headers = {"Content-Type": "application/json"}
    if provider == "openai":
        headers["Authorization"] = "Bearer " + key
        data = {"model": model, "input": prompt}
    elif provider == "anthropic":
        headers.update({"x-api-key": key, "anthropic-version": "2023-06-01"})
        data = {"model": model, "max_tokens": 1024, "messages": [{"role": "user", "content": prompt}]}
    elif provider == "gemini":
        headers["x-goog-api-key"] = key
        data = {"contents": [{"parts": [{"text": prompt}]}]}
    elif provider == "ollama":
        data = {"model": model, "messages": [{"role": "user", "content": prompt}], "stream": False}
    else:
        if key:
            headers["Authorization"] = "Bearer " + key
        data = {"model": model, "messages": [{"role": "user", "content": prompt}], "stream": False}
    return url, headers, data

def parse_response(provider, response):
    try:
        if provider == "openai":
            return "\n".join(part["text"] for item in response["output"] for part in item.get("content", []) if part.get("type") == "output_text")
        if provider == "anthropic":
            return "\n".join(x["text"] for x in response["content"] if x.get("type") == "text")
        if provider == "gemini":
            return "\n".join(x["text"] for x in response["candidates"][0]["content"]["parts"] if "text" in x)
        return response["message"]["content"] if provider == "ollama" else response["choices"][0]["message"]["content"]
    except (KeyError, IndexError, TypeError) as exc:
        raise ValueError("Unexpected provider response format") from exc

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=["list", "check", "ask"])
    parser.add_argument("--provider", choices=PROVIDERS)
    parser.add_argument("--model")
    parser.add_argument("--prompt")
    parser.add_argument("--endpoint")
    args = parser.parse_args()
    if args.action == "list":
        print(json.dumps({name: {"key_env": config["env"], "default_endpoint": config["url"]} for name, config in PROVIDERS.items()}, indent=2))
        return
    if not args.provider or not args.model:
        raise ValueError("Specify --provider and --model")
    # A check is deliberately offline and does not validate a paid account or make a request.
    prompt = args.prompt or ("Connection configuration preview" if args.action == "check" else "")
    url, headers, data = request_for(args.provider, args.model, prompt, args.endpoint)
    if args.action == "check":
        print(json.dumps({"provider": args.provider, "model": args.model, "endpoint": url, "key_present": bool(os.environ.get(PROVIDERS[args.provider]["env"], "")) if PROVIDERS[args.provider]["env"] else None, "network_called": False}, indent=2))
        return
    request = urllib.request.Request(url, json.dumps(data).encode("utf-8"), headers=headers, method="POST")
    try:
        with urllib.request.urlopen(request, timeout=45) as res:
            result = json.load(res)
    except (urllib.error.URLError, TimeoutError) as exc:
        raise ValueError("Provider request failed; check connectivity, model, key and quota") from exc
    print(parse_response(args.provider, result))

if __name__ == "__main__":
    try:
        main()
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        sys.exit(1)
