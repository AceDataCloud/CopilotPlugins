#!/usr/bin/env python3
"""Materialize five independently installable Agent Plugins from one catalog."""
import json
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parent.parent
CATALOG = json.loads((ROOT / 'catalog.json').read_text())
REPO = 'https://github.com/AceDataCloud/CopilotPlugins'
KEY_IMAGE = 'https://raw.githubusercontent.com/AceDataCloud/SunoDify/8d3d03570e73324220f111f7fe343da0792a8071/_assets/tutorial/get-api-key-en.png'
CREATE_IMAGE = 'https://raw.githubusercontent.com/AceDataCloud/SunoDify/8d3d03570e73324220f111f7fe343da0792a8071/_assets/tutorial/create-api-key-en.png'


def cta(path, content):
    return f'https://platform.acedata.cloud/{path}?utm_source=github_copilot&utm_medium=referral&utm_campaign=evergreen&utm_content={content}'


def main():
    entries = []
    for service in CATALOG['services']:
        slug, title = service['slug'], service['title']
        target = ROOT / 'plugins' / slug
        (target / 'scripts').mkdir(parents=True, exist_ok=True)
        skill = target / 'skills' / service['skill']
        skill.mkdir(parents=True, exist_ok=True)
        description = f'{title} by Ace Data Cloud: create {service["output"]}, query the same asynchronous task, and retrieve its final media link.'
        manifest = {'$schema':'https://agent-plugins.org/schemas/1.0.0/plugin.schema.json', 'name':slug,
                    'version':CATALOG['version'], 'description':description,
                    'author':{'name':'Ace Data Cloud','url':'https://github.com/AceDataCloud'},
                    'repository':REPO,'homepage':REPO,'license':'MIT','keywords':service['keywords']}
        mcp = {'$schema':'https://agent-plugins.org/schemas/1.0.0/mcp.schema.json', 'mcpServers':{
            'ace-'+service['id']:{'type':'stdio','command':'python3','args':['${PLUGIN_ROOT}/scripts/mcp_bridge.py']}}}
        for name, data in [('plugin.json',manifest),('mcp.json',mcp),('service.json',service)]:
            (target/name).write_text(json.dumps(data,indent=2)+'\n')
        shutil.copyfile(ROOT/'scripts/mcp_bridge.py',target/'scripts/mcp_bridge.py')
        inspect = (f'For a free first connection check, call `{service["inspect_tool"]}` only; this returns model metadata, not media.'
                   if service['inspect_tool'] else 'For a free first connection check, inspect the discovered tool names only; do not submit an image request.')
        skill_text = f'''---
name: {service['skill']}
description: 'Use {title} through Ace Data Cloud to create {service['output']}, inspect supported options, or retrieve a previously submitted task. Uses this plugin MCP connection and a user-owned service API key.'
---

# {title} by Ace Data Cloud

Use only the `ace-{service['id']}` MCP tools bundled with this plugin. Read the tool input schema before choosing model, dimensions, duration or quality; public supported model names and prices can change. {inspect}

For new {service['output']}, establish the user's requested output and applicable price/budget before invoking `{service['create_tool']}`. Submit once. If a task ID is returned, keep it and call `{service['query_tool']}` for that same ID until a terminal response is available; accepted/pending is not success. A timeout is not permission to submit again. For an existing task request, never call generation.

Report success only when the task reports terminal success and exposes its media URL. Return a clickable result link and task ID; distinguish preview, pending and failed results. Preserve upstream error meaning: authentication, insufficient credit, moderation and rate limits need their actual remedy, not an alternate model or retrying creation.

Keys are supplied privately by the environment. Never print a key, put it in a prompt, or write it into project files. This integration is provided by Ace Data Cloud, not the {title} service owner. See the plugin README for setup and paid-service requirements.
'''
        (skill/'SKILL.md').write_text(skill_text)
        var=service['id'].upper().replace('-','_')
        install=f'copilot plugin marketplace add AceDataCloud/CopilotPlugins\ncopilot plugin install {slug}@ace-data-cloud'
        example=(f'Use {service["inspect_tool"]} only. Do not generate media.' if service['inspect_tool'] else 'List the tools from ace-nano-banana. Do not call image generation.')
        task_example=f'Use {service["query_tool"]} only for task ID TASK_ID. Do not generate again. Report pending, failed or terminal success and return the media link if finished.'
        paths=', '.join('`'+x+'`' for x in service['api_paths'])
        icon_name='icon.jpg' if service['id']=='happyhorse' else 'icon.png'
        text=f'''# {title} by Ace Data Cloud for GitHub Copilot

![{title} service icon; integration provided by Ace Data Cloud](assets/{icon_name})

[简体中文](README.zh-CN.md)

A separately installable {title} plugin for Copilot CLI and repository cloud-agent plugin configuration. Ace Data Cloud provides this integration and its API access; this is not an official plugin from the {title} service owner. It does not change Copilot's LLM provider.

**Release status:** version {CATALOG['version']} is under source PR review. No listing in GitHub's built-in `awesome-copilot` marketplace is claimed. The commands below apply after the source PR is merged; before then reviewers can use the immutable PR SHA/path supplied in the review receipt. Installing a plugin does not buy service credits or start generation.

## 1. Install only this service

[GitHub's official plugin guide](https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/plugins-finding-installing) supports a marketplace plus individual plugin install:

```sh
{install}
```

Once an official listing is approved, its exact listing link and official install command will be added here. Until then this is Ace's public source marketplace, not GitHub's default catalog. Requires Copilot CLI with Agent Plugins 1.0 support, Python 3.10+, `uvx`, and HTTPS access to PyPI and `api.acedata.cloud`. The plugin reuses [`{service['package']}=={service['version']}`](https://pypi.org/project/{service['package']}/{service['version']}/); API implementation stays in [MCPs](https://github.com/AceDataCloud/MCPs), with a narrow {title} tool filter here.

## 2. Register or sign in and get the right key

1. Open [Ace Data Cloud Applications]({cta('console/applications',slug+'_key')}) and register/sign in. If necessary choose **Initialize General Application**.
2. Open **General application**, check {title} access, [current pricing]({cta('models',slug+'_pricing')}) and balance. Copy its API key, or choose **Manage Keys → Create** for a dedicated Copilot key.
3. Set expiry and restrictions appropriate to your workflow. If **Allowed APIs** is enabled, permit generation **and** task retrieval: {paths}. Copy the token value without `Bearer `; a `platform-...` management token is not a service API key.

![Existing real Ace console screenshot: copy API key or Manage Keys]({KEY_IMAGE})
![Existing real Ace console screenshot: create a dedicated key]({CREATE_IMAGE})

These are redacted Ace Console screenshots reused from the [SunoDify tutorial](https://github.com/AceDataCloud/SunoDify/blob/8d3d03570e73324220f111f7fe343da0792a8071/README.md), retrieved for this guide on 2026-10-18. The Dify-specific authorization controls are not Copilot controls; only the shared Ace key pages are reused.

## 3. Supply the key privately

For **Copilot CLI**, set `ACEDATACLOUD_{var}_API_TOKEN` in your private shell environment before starting Copilot. Use your shell/secret manager's protected entry method; do not put the value in a prompt or committed `.env`. The bridge also accepts `ACEDATACLOUD_API_TOKEN` as a shared-key option.

For the **GitHub repository cloud agent**, repository owners use **Settings → Security → Secrets and variables → Agents**, with secret name `COPILOT_MCP_{var}_API_TOKEN`. This is a service API key, not the Platform Token used by the separate account catalog MCP. Configure plugin enablement through `.github/copilot/settings.json`; the repository sample is in [examples](https://github.com/AceDataCloud/CopilotPlugins/blob/main/examples/README.md). These new plugins' cloud secret propagation and execution still require a real cloud acceptance run. Do not infer that a local install proved cloud access.

## 4. First connection and same-task result

No-cost setup prompt:

```text
{example}
```

When you explicitly authorize a priced generation, ask Copilot to use `{service['create_tool']}` once and inspect its current input schema. This guide intentionally does not hard-code a model/price or submit a paid sample. An accepted request may return only a task ID.

Use that same ID:

```text
{task_example}
```

Pending means wait and query the same task. Terminal success plus the final media URL is the expected result. Do not rerun generation to check status. No successful new media run is claimed for this plugin release.

## Troubleshooting

- Plugin missing: register `AceDataCloud/CopilotPlugins`, then install the exact `{slug}` entry; official catalog approval is separate.
- `uvx` or Python missing / package download fails: install those dependencies from official sources and check network access; do not insert an unrelated package or fallback model.
- Authentication error: confirm the **service API key**, its service/API scope and expiry. Never send the value in an issue.
- Insufficient balance: check [current usage]({cta('console/usage',slug+'_usage')}) and pricing before new work. No payment is performed automatically.
- Policy/secret unavailable in cloud: an existing administrator must confirm Copilot availability, plugin policy and Agents secret access; this plugin does not bypass policy.
- Task pending: query the saved ID. Moderation and rate-limit errors keep their upstream meaning.

## Boundaries and support

Only the names in `service.json` are exposed by the transport filter, including generation/editing operations for this service. Installing it does not imply permission for a paid request. No hooks, model provider changes, unattended generation, retries, OAuth flow or account write tools are installed. Report integration issues at [{REPO}/issues]({REPO}/issues), without credentials. Code: MIT; API usage has its own account/service terms.
'''
        (target/'README.md').write_text(text)
        zh=f'''# GitHub Copilot 的 {title} by Ace Data Cloud 插件

![{title} 服务图标，集成由 Ace Data Cloud 提供](assets/{icon_name})

[English](README.md)

这是 Ace Data Cloud 提供的独立 {title} 集成，不冒充该服务官方。只安装这一项即可获得对应工具与同任务查询指引；不会增加或替换 Copilot 的默认 LLM 提供商。

**当前状态：** 源码 PR 审核中，尚未宣称进入 GitHub 默认 `awesome-copilot` 目录。下列 main 安装入口需源码合并后才成立；审阅者可使用交付收据中的固定 PR SHA。安装不会自动生成或充值。

## 1. 安装单服务插件

按 [GitHub 官方安装方式](https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/plugins-finding-installing)：

```sh
{install}
```

当前是 Ace 自有公开源码 marketplace；官方收录另行审核，不把手动加目录算作官方默认发现。需支持 Agent Plugins 1.0 的 Copilot、Python 3.10+ 与 `uvx`。使用公开包 `{service['package']}=={service['version']}`；底层 API 仍由 MCPs 单一源码维护。

## 2. 注册、登录与 API Token

打开 [Ace Applications]({cta('console/applications',slug+'_zh_key')}) 注册/登录；没有通用应用时点 **Initialize General Application**。打开 **General application**，核对 {title} 权限、[当前价格]({cta('models',slug+'_zh_pricing')})和余额。直接复制已有 API key，或 **Manage Keys → Create** 创建独立 Copilot key；按需限制到期日、用量及 API。允许列表应含创建与查询：{paths}。

![真实 Ace 控制台原图：复制或管理 key]({KEY_IMAGE})
![真实 Ace 控制台原图：创建独立 key]({CREATE_IMAGE})

原图来自 SunoDify 的公共 Ace 密钥页面，2026-10-18 复用，凭据已遮蔽；不是 Dify 授权步骤移植，也不是新的 Copilot 界面截图。只复制 token 本身，不带 `Bearer `；`platform-...` 管理 token 不适用。

## 3. 在哪里粘贴/保存

CLI：在启动 Copilot 的私有 shell/secret manager 中设置 `ACEDATACLOUD_{var}_API_TOKEN`；不要发到 Chat 或提交 `.env`。也支持共享 `ACEDATACLOUD_API_TOKEN`。

仓库云端：管理员在 **Settings → Security → Secrets and variables → Agents** 使用 `COPILOT_MCP_{var}_API_TOKEN`，插件通过 `.github/copilot/settings.json` 启用；见[仓库样例](https://github.com/AceDataCloud/CopilotPlugins/blob/main/examples/README.md)。当前版本的真实云端 secret 注入及调用尚未验收，CLI 安装不能代替它。遵循组织策略，不擅改权限或扩权。

## 4. 首用、任务与结果

先做免费检查：`{example}`。如需新生成，先确认用户具体需求、当前模型 schema、价格和额度，再调用 `{service['create_tool']}` 一次；这里没有自动提交收费示例。

拿到 task ID 后，仅调用 `{service['query_tool']}` 查询同一个 ID，pending 则继续查询，不能重发生成。终态成功且返回最终媒体链接才算完成；失败保留上游原意。当前插件没有新生成结果或账单验收证明。

## 常见问题

找不到插件先确认已加入 Ace 目录并安装精确名称 `{slug}`；官方默认目录收录是另一阶段。缺 Python/uvx 或包下载失败先修依赖网络，不随意换包/模型。认证失败核对服务 API key 的权限、过期日和 API 限制；余额不足先读当前价格与[用量]({cta('console/usage',slug+'_zh_usage')})。云端受限由现有管理员核策略与 Agents secret，不绕过。工具过滤只暴露 `service.json` 明列名称；安装并非收费授权，无自动重试、账户写入或未授权生成。
'''
        (target/'README.zh-CN.md').write_text(zh)
        entries.append({**{key:manifest[key] for key in ['name','version','description','author','homepage','repository','license','keywords']},'source':'./plugins/'+slug})
    marketplace={'name':'ace-data-cloud','owner':{'name':'Ace Data Cloud','email':'dev@acedata.cloud'},'metadata':{'description':'Independent Suno, Seedance, HappyHorse, GPT Image and Nano Banana integrations for GitHub Copilot.','version':CATALOG['version']},'plugins':entries}
    p=ROOT/'.github/plugin';p.mkdir(parents=True,exist_ok=True);(p/'marketplace.json').write_text(json.dumps(marketplace,indent=2)+'\n')


if __name__=='__main__':
    main()
