#!/usr/bin/env python3
"""Verify native Copilot plugin installation from a published public Git tag.

Run in a disposable COPILOT_HOME/cache. No credentials, model session, MCP tool
call or generation is needed. This is a public-source install, not proof of an
awesome-copilot listing or cloud execution.
"""

import argparse
import datetime
import json
import re
import subprocess
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tag", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if not re.fullmatch(r"v[0-9]+\.[0-9]+\.[0-9]+", args.tag):
        parser.error("Use an exact published vMAJOR.MINOR.PATCH tag")

    catalog = json.loads((Path(__file__).resolve().parents[1] / "catalog.json").read_text())
    services = catalog["services"]
    commands = [
        ["--version"],
        ["plugin", "marketplace", "add", "AceDataCloud/CopilotPlugins#" + args.tag],
        ["plugin", "marketplace", "browse", "ace-data-cloud", "--json"],
        *[["plugin", "install", service["slug"] + "@ace-data-cloud"] for service in services],
        ["plugin", "list", "--json"],
        ["mcp", "list", "--json"],
    ]
    report = {
        "checked_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "tag": args.tag, "source": "public GitHub release via native Copilot commands",
        "credentials_supplied": False, "inference_started": False,
        "generation_calls": 0, "commands": [], "status": "FAIL",
    }
    try:
        for command in commands:
            result = subprocess.run(["copilot", *command], text=True, capture_output=True, timeout=90)
            report["commands"].append({"args": command, "exit_code": result.returncode,
                                       "stdout": result.stdout, "stderr": result.stderr})
            if result.returncode:
                raise RuntimeError("Copilot command failed: " + " ".join(command))
        installed = json.loads(report["commands"][-2]["stdout"])
        servers = json.loads(report["commands"][-1]["stdout"])["mcpServers"]
        for service in services:
            matching = [p for p in installed if p["name"] == service["slug"]]
            if len(matching) != 1 or not matching[0]["enabled"] or matching[0]["version"] != args.tag[1:]:
                raise RuntimeError("Published plugin/version not installed: " + service["slug"])
            config = servers.get("ace-" + service["id"], {})
            if config.get("sourcePlugin") != service["slug"] or config.get("source") != "plugin":
                raise RuntimeError("MCP connection not registered: " + service["slug"])
        report["status"] = "PASS"
        report["plugins_installed"] = len(services)
        report["mcp_connections_registered"] = len(services)
    except Exception as error:
        report["error"] = str(error)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({key: value for key, value in report.items() if key != "commands"}, indent=2))
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
