# Independent service plugins for GitHub Copilot

Five separately installable integrations provided by **Ace Data Cloud**:

| Plugin | Use | Setup |
| --- | --- | --- |
| Suno by Ace Data Cloud | Music generation and existing audio-task lookup | [English](plugins/suno-by-ace-data-cloud/README.md) / [中文](plugins/suno-by-ace-data-cloud/README.zh-CN.md) |
| Seedance by Ace Data Cloud | Video generation and same-task lookup | [English](plugins/seedance-by-ace-data-cloud/README.md) / [中文](plugins/seedance-by-ace-data-cloud/README.zh-CN.md) |
| HappyHorse by Ace Data Cloud | Video generation and same-task lookup | [English](plugins/happyhorse-by-ace-data-cloud/README.md) / [中文](plugins/happyhorse-by-ace-data-cloud/README.zh-CN.md) |
| GPT Image by Ace Data Cloud | Image generation/editing and same-task lookup | [English](plugins/gpt-image-by-ace-data-cloud/README.md) / [中文](plugins/gpt-image-by-ace-data-cloud/README.zh-CN.md) |
| Nano Banana by Ace Data Cloud | Image generation/editing and same-task lookup | [English](plugins/nano-banana-by-ace-data-cloud/README.md) / [中文](plugins/nano-banana-by-ace-data-cloud/README.zh-CN.md) |

The source implementation is under PR review. Official `awesome-copilot`
marketplace approval, real cloud execution and paid media acceptance are separate
stages; none are implied by a repository or installation test. This does not add
Ace to Copilot's default LLM provider picker. These are Ace integrations, not
official plugins from the named model/service owners.

## Install one service after source publication

```sh
copilot plugin marketplace add AceDataCloud/CopilotPlugins
copilot plugin install suno-by-ace-data-cloud@ace-data-cloud
```

Until the source PR merges these `main` commands do not install its new files.
Reviewers can inspect and install from the pinned PR commit using the review
receipt. Every plugin has an Agent Plugins 1.0 manifest, a bundled Skill, one
stdio MCP connection and a narrow tool filter; API behavior is provided by pinned
published [Ace MCP packages](https://github.com/AceDataCloud/MCPs), not duplicated
API clients. Requires Python 3.10+, `uvx`, and Copilot with Agent Plugins support.
The current build was checked against Copilot CLI 1.0.98.

For the cloud route see [repository configuration](examples/README.md). No sample
configuration is activated here; secrets, access policies and budgets must be
reviewed independently. Key setup uses real redacted Ace Console screenshots in
each English/Chinese guide. No generated interface or fake terminal image is used.

## Development

```sh
python3 scripts/build_plugins.py
python3 -m unittest discover -s tests -v
git diff --check
```

Catalog, bridge and builder are the sources of the materialized packages. All
checks are local, use a fake MCP process where needed and submit no paid requests.
Use an isolated `COPILOT_HOME`/`COPILOT_CACHE_HOME` for install verification so
testing does not alter a user's real plugin setup. Do not start inference for an
installation-only check.
Independent Suno, Seedance, HappyHorse, GPT Image and Nano Banana plugins for GitHub Copilot, provided by Ace Data Cloud.
