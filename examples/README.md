# Repository cloud plugin configuration

GitHub documents repository plugin enablement in
[`enabledPlugins` and `extraKnownMarketplaces`](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-config-dir-reference#repository-settings-githubcopilotsettingsjson).
This example is **not activated in this repository** and no cloud task has been
started. Do not overwrite an existing repository settings file: merge only the
chosen service entry after administrator review, publication and budget checks.

After an official default-marketplace listing is approved, use its exact plugin
ID there. Until then, the documented alternative is a user-added marketplace:

```json
{
  "extraKnownMarketplaces": {
    "ace-data-cloud": {
      "source": {
        "source": "github",
        "repo": "AceDataCloud/CopilotPlugins"
      }
    }
  },
  "enabledPlugins": {
    "suno-by-ace-data-cloud@ace-data-cloud": true
  }
}
```

The public Ace source catalog and versioned Git release are independent of
GitHub's default marketplace approval. Pin the reviewed Git SHA/tag for a
repeatable installation. This example still has no cloud execution receipt.

For cloud execution the repository administrator must first confirm cloud agent
availability, plugin policy, the allowed test repository, an existing seat and a
single-session AI/runner allowance. Agents secrets use a service-specific name,
for example `COPILOT_MCP_SUNO_API_TOKEN`; the plugin bridge maps it to the
underlying package's `ACEDATACLOUD_API_TOKEN`. Whether that MCP-only secret reaches
the plugin stdio process in the current cloud runtime still needs real acceptance.
If it does not, stop and record the actual configuration contract—do not expose it
as a normal variable, echo it, or bypass the policy.

Installing a plugin can expose paid generation tools. Do not enable one in an
unattended repository unless its service access and allowed actions are deliberate.
No hooks or automatic generation are shipped. For an existing task, call the
matching `*_get_task` only; never submit again to check progress.

Need an image for the setup guide? Capture the real plugin install/list page and
repository Agents-secret **name only** with the coordinating browser owner. The
old VS Code screenshots do not prove this cloud plugin installation.
