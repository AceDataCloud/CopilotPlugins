# CopilotPlugins

Independent service plugins for GitHub Copilot. The API implementations remain
in AceDataCloud/MCPs; this repository packages pinned published MCPs, narrow tool
boundaries and Copilot-specific instructions. Do not copy or fork API clients.

- Edit `catalog.json`, `scripts/mcp_bridge.py` and `scripts/build_plugins.py`, then
  run `python3 scripts/build_plugins.py`. Materialized plugin files are generated.
- Run `python3 -m unittest discover -s tests -v` and `git diff --check`.
- Installation/schema tests must use temporary Copilot home/cache directories and
  must not start inference or paid generation.
- Never commit a credential. Media plugins use service API keys, not Platform Tokens.
- Do not claim an official marketplace listing until an exact accepted entry exists.
- Never merge PRs, modify user/repository secrets or policies, or submit paid tasks
  without the user's applicable authorization.
