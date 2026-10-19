---
name: suno-music
description: 'Use Suno through Ace Data Cloud to create audio, inspect supported options, or retrieve a previously submitted task. Uses this plugin MCP connection and a user-owned service API key.'
---

# Suno by Ace Data Cloud

Use only the `ace-suno` MCP tools bundled with this plugin. Read the tool input schema before choosing model, dimensions, duration or quality; public supported model names and prices can change. For a free first connection check, call `suno_list_models` only; this returns model metadata, not media.

For new audio, establish the user's requested output and applicable price/budget before invoking `suno_generate_music`. Submit once. If a task ID is returned, keep it and call `suno_get_task` for that same ID until a terminal response is available; accepted/pending is not success. A timeout is not permission to submit again. For an existing task request, never call generation.

Report success only when the task reports terminal success and exposes its media URL. Return a clickable result link and task ID; distinguish preview, pending and failed results. Preserve upstream error meaning: authentication, insufficient credit, moderation and rate limits need their actual remedy, not an alternate model or retrying creation.

Keys are supplied privately by the environment. Never print a key, put it in a prompt, or write it into project files. This integration is provided by Ace Data Cloud, not the Suno service owner. See the plugin README for setup and paid-service requirements.
