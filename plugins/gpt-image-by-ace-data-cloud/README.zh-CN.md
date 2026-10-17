# GitHub Copilot 的 GPT Image by Ace Data Cloud 插件

![GPT Image 服务图标，集成由 Ace Data Cloud 提供](assets/icon.png)

[English](README.md)

这是 Ace Data Cloud 提供的独立 GPT Image 集成，不冒充该服务官方。只安装这一项即可获得对应工具与同任务查询指引；不会增加或替换 Copilot 的默认 LLM 提供商。

**当前状态：** 源码 PR 审核中，尚未宣称进入 GitHub 默认 `awesome-copilot` 目录。下列 main 安装入口需源码合并后才成立；审阅者可使用交付收据中的固定 PR SHA。安装不会自动生成或充值。

## 1. 安装单服务插件

按 [GitHub 官方安装方式](https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/plugins-finding-installing)：

```sh
copilot plugin marketplace add AceDataCloud/CopilotPlugins
copilot plugin install gpt-image-by-ace-data-cloud@ace-data-cloud
```

当前是 Ace 自有公开源码 marketplace；官方收录另行审核，不把手动加目录算作官方默认发现。需支持 Agent Plugins 1.0 的 Copilot、Python 3.10+ 与 `uvx`。使用公开包 `mcp-openai-pro==2026.10.17.0`；底层 API 仍由 MCPs 单一源码维护。

## 2. 注册、登录与 API Token

打开 [Ace Applications](https://platform.acedata.cloud/console/applications?utm_source=github_copilot&utm_medium=referral&utm_campaign=evergreen&utm_content=gpt-image-by-ace-data-cloud_zh_key) 注册/登录；没有通用应用时点 **Initialize General Application**。打开 **General application**，核对 GPT Image 权限、[当前价格](https://platform.acedata.cloud/models?utm_source=github_copilot&utm_medium=referral&utm_campaign=evergreen&utm_content=gpt-image-by-ace-data-cloud_zh_pricing)和余额。直接复制已有 API key，或 **Manage Keys → Create** 创建独立 Copilot key；按需限制到期日、用量及 API。允许列表应含创建与查询：`/openai/images/generations`, `/openai/images/edits`, `/openai/tasks`。

![真实 Ace 控制台原图：复制或管理 key](https://raw.githubusercontent.com/AceDataCloud/SunoDify/8d3d03570e73324220f111f7fe343da0792a8071/_assets/tutorial/get-api-key-en.png)
![真实 Ace 控制台原图：创建独立 key](https://raw.githubusercontent.com/AceDataCloud/SunoDify/8d3d03570e73324220f111f7fe343da0792a8071/_assets/tutorial/create-api-key-en.png)

原图来自 SunoDify 的公共 Ace 密钥页面，2026-10-18 复用，凭据已遮蔽；不是 Dify 授权步骤移植，也不是新的 Copilot 界面截图。只复制 token 本身，不带 `Bearer `；`platform-...` 管理 token 不适用。

## 3. 在哪里粘贴/保存

CLI：在启动 Copilot 的私有 shell/secret manager 中设置 `ACEDATACLOUD_GPT_IMAGE_API_TOKEN`；不要发到 Chat 或提交 `.env`。也支持共享 `ACEDATACLOUD_API_TOKEN`。

仓库云端：管理员在 **Settings → Security → Secrets and variables → Agents** 使用 `COPILOT_MCP_GPT_IMAGE_API_TOKEN`，插件通过 `.github/copilot/settings.json` 启用；见[仓库样例](https://github.com/AceDataCloud/CopilotPlugins/blob/main/examples/README.md)。当前版本的真实云端 secret 注入及调用尚未验收，CLI 安装不能代替它。遵循组织策略，不擅改权限或扩权。

## 4. 首用、任务与结果

先做免费检查：`Use openai_list_image_models only. Do not generate media.`。如需新生成，先确认用户具体需求、当前模型 schema、价格和额度，再调用 `openai_generate_image` 一次；这里没有自动提交收费示例。

拿到 task ID 后，仅调用 `openai_get_task` 查询同一个 ID，pending 则继续查询，不能重发生成。终态成功且返回最终媒体链接才算完成；失败保留上游原意。当前插件没有新生成结果或账单验收证明。

## 常见问题

找不到插件先确认已加入 Ace 目录并安装精确名称 `gpt-image-by-ace-data-cloud`；官方默认目录收录是另一阶段。缺 Python/uvx 或包下载失败先修依赖网络，不随意换包/模型。认证失败核对服务 API key 的权限、过期日和 API 限制；余额不足先读当前价格与[用量](https://platform.acedata.cloud/console/usage?utm_source=github_copilot&utm_medium=referral&utm_campaign=evergreen&utm_content=gpt-image-by-ace-data-cloud_zh_usage)。云端受限由现有管理员核策略与 Agents secret，不绕过。工具过滤只暴露 `service.json` 明列名称；安装并非收费授权，无自动重试、账户写入或未授权生成。
