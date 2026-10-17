# HappyHorse by Ace Data Cloud for GitHub Copilot

[简体中文](README.zh-CN.md)

A separately installable HappyHorse plugin for Copilot CLI and repository cloud-agent plugin configuration. Ace Data Cloud provides this integration and its API access; this is not an official plugin from the HappyHorse service owner. It does not change Copilot's LLM provider.

**Release status:** version 0.1.0 is under source PR review. No listing in GitHub's built-in `awesome-copilot` marketplace is claimed. The commands below apply after the source PR is merged; before then reviewers can use the immutable PR SHA/path supplied in the review receipt. Installing a plugin does not buy service credits or start generation.

## 1. Install only this service

[GitHub's official plugin guide](https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/plugins-finding-installing) supports a marketplace plus individual plugin install:

```sh
copilot plugin marketplace add AceDataCloud/CopilotPlugins
copilot plugin install happyhorse-by-ace-data-cloud@ace-data-cloud
```

Once an official listing is approved, its exact listing link and official install command will be added here. Until then this is Ace's public source marketplace, not GitHub's default catalog. Requires Copilot CLI with Agent Plugins 1.0 support, Python 3.10+, `uvx`, and HTTPS access to PyPI and `api.acedata.cloud`. The plugin reuses [`mcp-happyhorse==2026.10.12.0`](https://pypi.org/project/mcp-happyhorse/2026.10.12.0/); API implementation stays in [MCPs](https://github.com/AceDataCloud/MCPs), with a narrow HappyHorse tool filter here.

## 2. Register or sign in and get the right key

1. Open [Ace Data Cloud Applications](https://platform.acedata.cloud/console/applications?utm_source=github_copilot&utm_medium=referral&utm_campaign=evergreen&utm_content=happyhorse-by-ace-data-cloud_key) and register/sign in. If necessary choose **Initialize General Application**.
2. Open **General application**, check HappyHorse access, [current pricing](https://platform.acedata.cloud/models?utm_source=github_copilot&utm_medium=referral&utm_campaign=evergreen&utm_content=happyhorse-by-ace-data-cloud_pricing) and balance. Copy its API key, or choose **Manage Keys → Create** for a dedicated Copilot key.
3. Set expiry and restrictions appropriate to your workflow. If **Allowed APIs** is enabled, permit generation **and** task retrieval: `/happyhorse/videos`, `/happyhorse/tasks`. Copy the token value without `Bearer `; a `platform-...` management token is not a service API key.

![Existing real Ace console screenshot: copy API key or Manage Keys](https://raw.githubusercontent.com/AceDataCloud/SunoDify/8d3d03570e73324220f111f7fe343da0792a8071/_assets/tutorial/get-api-key-en.png)
![Existing real Ace console screenshot: create a dedicated key](https://raw.githubusercontent.com/AceDataCloud/SunoDify/8d3d03570e73324220f111f7fe343da0792a8071/_assets/tutorial/create-api-key-en.png)

These are redacted Ace Console screenshots reused from the [SunoDify tutorial](https://github.com/AceDataCloud/SunoDify/blob/8d3d03570e73324220f111f7fe343da0792a8071/README.md), retrieved for this guide on 2026-10-18. The Dify-specific authorization controls are not Copilot controls; only the shared Ace key pages are reused.

## 3. Supply the key privately

For **Copilot CLI**, set `ACEDATACLOUD_HAPPYHORSE_API_TOKEN` in your private shell environment before starting Copilot. Use your shell/secret manager's protected entry method; do not put the value in a prompt or committed `.env`. The bridge also accepts `ACEDATACLOUD_API_TOKEN` as a shared-key option.

For the **GitHub repository cloud agent**, repository owners use **Settings → Security → Secrets and variables → Agents**, with secret name `COPILOT_MCP_HAPPYHORSE_API_TOKEN`. This is a service API key, not the Platform Token used by the separate account catalog MCP. Configure plugin enablement through `.github/copilot/settings.json`; the repository sample is in [examples](https://github.com/AceDataCloud/CopilotPlugins/blob/main/examples/README.md). These new plugins' cloud secret propagation and execution still require a real cloud acceptance run. Do not infer that a local install proved cloud access.

## 4. First connection and same-task result

No-cost setup prompt:

```text
Use happyhorse_list_models only. Do not generate media.
```

When you explicitly authorize a priced generation, ask Copilot to use `happyhorse_generate_video` once and inspect its current input schema. This guide intentionally does not hard-code a model/price or submit a paid sample. An accepted request may return only a task ID.

Use that same ID:

```text
Use happyhorse_get_task only for task ID TASK_ID. Do not generate again. Report pending, failed or terminal success and return the media link if finished.
```

Pending means wait and query the same task. Terminal success plus the final media URL is the expected result. Do not rerun generation to check status. No successful new media run is claimed for this plugin release.

## Troubleshooting

- Plugin missing: register `AceDataCloud/CopilotPlugins`, then install the exact `happyhorse-by-ace-data-cloud` entry; official catalog approval is separate.
- `uvx` or Python missing / package download fails: install those dependencies from official sources and check network access; do not insert an unrelated package or fallback model.
- Authentication error: confirm the **service API key**, its service/API scope and expiry. Never send the value in an issue.
- Insufficient balance: check [current usage](https://platform.acedata.cloud/console/usage?utm_source=github_copilot&utm_medium=referral&utm_campaign=evergreen&utm_content=happyhorse-by-ace-data-cloud_usage) and pricing before new work. No payment is performed automatically.
- Policy/secret unavailable in cloud: an existing administrator must confirm Copilot availability, plugin policy and Agents secret access; this plugin does not bypass policy.
- Task pending: query the saved ID. Moderation and rate-limit errors keep their upstream meaning.

## Boundaries and support

Only the names in `service.json` are exposed by the transport filter, including generation/editing operations for this service. Installing it does not imply permission for a paid request. No hooks, model provider changes, unattended generation, retries, OAuth flow or account write tools are installed. Report integration issues at [https://github.com/AceDataCloud/CopilotPlugins/issues](https://github.com/AceDataCloud/CopilotPlugins/issues), without credentials. Code: MIT; API usage has its own account/service terms.
