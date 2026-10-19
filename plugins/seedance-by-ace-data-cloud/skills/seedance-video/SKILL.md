---
name: seedance-video
description: 'Use Seedance through Ace Data Cloud to create video, inspect supported options, or retrieve a previously submitted task. Uses this plugin MCP connection and a user-owned service API key.'
---

# Seedance by Ace Data Cloud

Use only the `ace-seedance` MCP tools bundled with this plugin. Read the tool input schema before choosing model, dimensions, duration or quality; public supported model names and prices can change. For a free first connection check, call `seedance_list_models` only; this returns model metadata, not media.

For new video, establish the user's requested output and applicable price/budget before invoking `seedance_generate_video`. Submit once. If a task ID is returned, keep it and call `seedance_get_task` for that same ID until a terminal response is available; accepted/pending is not success. A timeout is not permission to submit again. For an existing task request, never call generation.

Report success only when the task reports terminal success and exposes its media URL. Return a clickable result link and task ID; distinguish preview, pending and failed results. Preserve upstream error meaning: authentication, insufficient credit, moderation and rate limits need their actual remedy, not an alternate model or retrying creation.

Keys are supplied privately by the environment. Never print a key, put it in a prompt, or write it into project files. This integration is provided by Ace Data Cloud, not the Seedance service owner. See the plugin README for setup and paid-service requirements.
