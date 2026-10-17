#!/usr/bin/env python3
"""Run a published Ace MCP package with one service's explicit tool boundary.

This is a stdio transport filter, not an API implementation. It never creates
tasks on its own, retries requests, or logs credentials or request payloads.
"""

import argparse
import json
import os
from pathlib import Path
import subprocess
import sys
import threading


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--inspect", action="store_true", help="Print package/tool metadata without starting MCP")
    args = parser.parse_args()
    spec = json.loads((Path(__file__).resolve().parent.parent / "service.json").read_text())
    if args.inspect:
        print(json.dumps({key: spec[key] for key in ("id", "package", "version", "tools")}, indent=2))
        return 0

    service_name = spec["id"].upper().replace("-", "_")
    keys = (f"ACEDATACLOUD_{service_name}_API_TOKEN", f"COPILOT_MCP_{service_name}_API_TOKEN", "ACEDATACLOUD_API_TOKEN")
    token = next((os.environ[key].strip() for key in keys if os.environ.get(key, "").strip()), "")
    if not token:
        print(f"Set {keys[0]} in your private environment before starting this plugin.", file=sys.stderr)
        return 2
    if token.startswith("platform-"):
        print("This media plugin requires a service API key, not a Platform Token.", file=sys.stderr)
        return 2

    env = {**os.environ, "ACEDATACLOUD_API_TOKEN": token}
    # Avoid an unrelated local .env changing the published package's settings.
    env["PYTHON_DOTENV_DISABLED"] = "1"
    try:
        child = subprocess.Popen(
            ["uvx", "--from", f"{spec['package']}=={spec['version']}", spec["package"]],
            stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=sys.stderr,
            text=True, bufsize=1, env=env,
        )
    except OSError as error:
        print(f"Cannot start the pinned MCP package: {type(error).__name__}. Check Python, uvx and network access.", file=sys.stderr)
        return 2

    allowed = set(spec["tools"])
    lock = threading.Lock()
    discovery_ids = set()

    def emit(message):
        with lock:
            sys.stdout.write(json.dumps(message, separators=(",", ":")) + "\n")
            sys.stdout.flush()

    def read_child():
        for line in child.stdout:
            try:
                message = json.loads(line)
            except (ValueError, TypeError):
                continue  # stdout is JSON-RPC only; do not surface arbitrary upstream logs.
            with lock:
                discovery = message.get("id") in discovery_ids
                if discovery:
                    discovery_ids.discard(message["id"])
            result = message.get("result")
            if discovery and isinstance(result, dict) and isinstance(result.get("tools"), list):
                result["tools"] = [tool for tool in result["tools"] if tool.get("name") in allowed]
            emit(message)

    reader = threading.Thread(target=read_child, daemon=True)
    reader.start()
    try:
        for line in sys.stdin:
            try:
                message = json.loads(line)
            except ValueError:
                emit({"jsonrpc": "2.0", "id": None, "error": {"code": -32700, "message": "Parse error"}})
                continue
            if not isinstance(message, dict):
                emit({"jsonrpc": "2.0", "id": None, "error": {"code": -32600, "message": "Invalid Request"}})
                continue
            method = message.get("method")
            params = message.get("params") or {}
            if method == "tools/call" and (not isinstance(params, dict) or params.get("name") not in allowed):
                if "id" in message:
                    emit({"jsonrpc": "2.0", "id": message["id"], "error": {"code": -32601, "message": "Tool is outside this service plugin"}})
                continue
            if method == "tools/list":
                with lock:
                    discovery_ids.add(message.get("id"))
            child.stdin.write(json.dumps(message, separators=(",", ":")) + "\n")
            child.stdin.flush()
    except (BrokenPipeError, KeyboardInterrupt):
        pass
    finally:
        try:
            child.stdin.close()
        except BrokenPipeError:
            pass
        reader.join(timeout=3)
        if child.poll() is None:
            child.terminate()
            child.wait(timeout=5)
    return child.returncode if child.returncode is not None else 1


if __name__ == "__main__":
    raise SystemExit(main())
