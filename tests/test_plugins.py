import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]


class PluginTests(unittest.TestCase):
    def test_bridge_filters_discovery_and_blocks_other_tools(self):
        with tempfile.TemporaryDirectory() as tmp:
            bin_dir = Path(tmp)
            fake_uvx = bin_dir / "uvx"
            fake_uvx.write_text("""#!/usr/bin/env python3
import sys,json
for line in sys.stdin:
    x=json.loads(line)
    if x.get('method')=='tools/list':
        result={'tools':[{'name':'openai_generate_image'},{'name':'openai_get_task'},{'name':'openai_chat_completion'}]}
    elif x.get('method')=='tools/call':
        result={'content':[{'type':'text','text':x['params']['name']}]}
    else:
        result={}
    if 'id' in x:
        print(json.dumps({'jsonrpc':'2.0','id':x['id'],'result':result}),flush=True)
""")
            fake_uvx.chmod(0o755)
            messages = [
                {"jsonrpc": "2.0", "id": 1, "method": "tools/list"},
                {"jsonrpc": "2.0", "id": 2, "method": "tools/call", "params": {"name": "openai_chat_completion"}},
                {"jsonrpc": "2.0", "id": 3, "method": "tools/call", "params": {"name": "openai_get_task", "arguments": {"task_id": "existing-test-task"}}},
            ]
            env = {**os.environ, "PATH": str(bin_dir) + os.pathsep + os.environ["PATH"],
                   "ACEDATACLOUD_GPT_IMAGE_API_TOKEN": "unit-test-only-not-a-secret"}
            result = subprocess.run(["python3", str(ROOT / "plugins/gpt-image-by-ace-data-cloud/scripts/mcp_bridge.py")],
                                    input="\n".join(json.dumps(x) for x in messages) + "\n",
                                    capture_output=True, text=True, env=env, timeout=15)
            self.assertEqual(result.returncode, 0, result.stderr)
            replies = {x["id"]: x for x in map(json.loads, result.stdout.splitlines())}
            self.assertEqual([x["name"] for x in replies[1]["result"]["tools"]], ["openai_generate_image", "openai_get_task"])
            self.assertEqual(replies[2]["error"]["code"], -32601)
            self.assertEqual(replies[3]["result"]["content"][0]["text"], "openai_get_task")
            self.assertNotIn("unit-test-only-not-a-secret", result.stdout + result.stderr)

    def test_missing_key_stops_before_package_start(self):
        env = {k: v for k, v in os.environ.items() if not k.startswith(("ACEDATACLOUD_", "COPILOT_MCP_"))}
        result = subprocess.run(["python3", str(ROOT / "plugins/suno-by-ace-data-cloud/scripts/mcp_bridge.py")],
                                input="", capture_output=True, text=True, env=env)
        self.assertEqual(result.returncode, 2)
        self.assertEqual(result.stdout, "")
        self.assertIn("ACEDATACLOUD_SUNO_API_TOKEN", result.stderr)

    def test_platform_token_rejected_before_package_start(self):
        env = {**os.environ, "ACEDATACLOUD_SUNO_API_TOKEN": "platform-unit-test-only"}
        result = subprocess.run(["python3", str(ROOT / "plugins/suno-by-ace-data-cloud/scripts/mcp_bridge.py")],
                                input="", capture_output=True, text=True, env=env)
        self.assertEqual(result.returncode, 2)
        self.assertNotIn("platform-unit-test-only", result.stdout + result.stderr)

    def test_all_five_plugins_inspect_without_starting_or_credentials(self):
        for service in json.loads((ROOT / "catalog.json").read_text())["services"]:
            with self.subTest(service=service["id"]):
                plugin = ROOT / "plugins" / service["slug"]
                result = subprocess.run(["python3", str(plugin / "scripts/mcp_bridge.py"), "--inspect"],
                                        capture_output=True, text=True, timeout=5)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual(json.loads(result.stdout)["package"], service["package"])
                self.assertTrue((plugin / "skills" / service["skill"] / "SKILL.md").is_file())


if __name__ == "__main__":
    unittest.main()
