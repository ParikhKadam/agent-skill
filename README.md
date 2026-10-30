# agent-skill

A Claude Code plugin marketplace: skills today, MCP servers, plugins and `CLAUDE.md` files as they come.

## Install

```
/plugin marketplace add ParikhKadam/agent-skill
/plugin install clarity-planning@agent-skill
/plugin install feature-plan@agent-skill
```

## Plugins

| Plugin | Skills | Status |
|---|---|---|
| [`clarity-planning`](plugins/clarity-planning) | `clarity-planning` (hub, shared tools and guides), `plan-clarity`, `plan-components`, `plan-flows`, `plan-build`, `plan-change`, `plan-review` | In use |
| [`feature-plan`](plugins/feature-plan) | `feature-plan`, `slice-spec` | Draft, tested on one scenario; names not final |

## Layout

```
.claude-plugin/marketplace.json     marketplace catalog (lists every plugin)
plugins/<plugin>/
  .claude-plugin/plugin.json        plugin manifest
  skills/<skill>/SKILL.md           one folder per skill, with its own references/scripts/assets
  (later) .mcp.json, agents/, commands/, hooks/
claude-md/                          (planned) reusable CLAUDE.md files
mcp/                                (planned) standalone MCP servers
```

Rules:
- One plugin per set of skills that work together. Skills inside a plugin may refer to each other with relative paths (`../clarity-planning/references/...`), so keep them as siblings under `skills/`.
- Anything a skill needs lives inside its own folder. Nothing points outside the plugin.
- Test runs and evals are not published here.
- Adding a plugin: create `plugins/<name>/` with a `plugin.json`, then add an entry to `marketplace.json`.
