# skill-sa

A focused Solution Architect plugin for Claude Code. Start with one architecture question, then create only the advice or artifacts that the decision actually needs.

`skill-sa` helps you:

- frame architecture problems and measurable drivers
- compare credible solution options
- record important decisions
- describe system structure and runtime behaviour
- define API, event, and data ownership contracts
- review whether a design is coherent and ready to build

## Install

### From Claude Code

Run these commands inside a Claude Code session:

```text
/plugin marketplace add phubkhn/skill-sa
/plugin install sa@skill-sa
/reload-plugins
```

The default installation scope is `user`, so the plugin is available in all your projects.

Verify the installation:

```text
/sa:architect Review this repository and identify its most important architecture risk.
```

You can also run `/plugin` and check that `sa@skill-sa` appears in the **Installed** tab.

### From the terminal

```bash
claude plugin marketplace add phubkhn/skill-sa --scope user
claude plugin install sa@skill-sa --scope user
claude plugin list
```

Choose the scope that matches how you want to use the plugin:

| Scope | Use when |
|---|---|
| `user` | You want the plugin in all your projects. This is the default. |
| `project` | The repository should share the plugin configuration with the team. |
| `local` | You want the plugin only for yourself in the current repository. |

## Update an installed plugin

Refresh the marketplace, update the plugin in the same scope in which it was installed, then restart Claude Code:

```bash
claude plugin marketplace update skill-sa
claude plugin update sa@skill-sa --scope user
```

Replace `user` with `project` or `local` when applicable. If a Claude Code session is already open, run:

```text
/reload-plugins
```

Third-party marketplaces do not enable automatic updates by default. To opt in, open `/plugin`, select **Marketplaces**, choose `skill-sa`, and enable auto-update.

## Start here

Use `/sa:architect` for normal architecture work. You do not need to choose a process step first.

```text
/sa:architect Review this repository and recommend the smallest architecture change for checkout retries.

/sa:architect Compare synchronous and event-driven order ingestion and create a concise architecture brief.

/sa:architect We are adding a public API used by two teams. Identify the architecture work we actually need.
```

The skill selects the smallest useful mode:

| Mode | Result |
|---|---|
| `quick` | Advice or analysis in the conversation; no files. |
| `brief` | One concise `architecture-brief.md`. |
| `artifact` | Only the requested or justified specialist artifact. |

`sa-config.yaml` is optional. Without it, the plugin follows the repository's existing conventions or writes architecture documents under `docs/architecture`.

## Core skills

| Command | Use it for | Typical output |
|---|---|---|
| `/sa:architect` | Frame the problem, inspect the repository, compare options, and recommend a solution | Advice or `architecture-brief.md` |
| `/sa:adr` | Preserve one consequential decision and its trade-offs | ADR |
| `/sa:hld` | Describe boundaries, responsibilities, dependencies, or deployment | Focused C4 or deployment view |
| `/sa:flow` | Explain one important runtime scenario and its failures | Sequence diagram and optional narrative |
| `/sa:interface` | Define a synchronous API or asynchronous event contract | OpenAPI or AsyncAPI |
| `/sa:data` | Define ownership, lifecycle, consistency, or migration | Data design and optional migration plan |
| `/sa:review` | Challenge an existing design independently | Findings and readiness verdict |

`/sa:method` explains the shared method but is normally internal.

## Simplified flow

```text
architect → decide and describe → review
              ├─ adr
              ├─ hld
              ├─ flow
              ├─ interface
              └─ data
```

The specialist skills are independent tools, not mandatory phases. Create an artifact only when it preserves an important decision, explains non-obvious behaviour, or defines a boundary another consumer depends on.

## Optional configuration

Add `sa-config.yaml` only when the repository needs explicit defaults:

```yaml
mode: brief
language: en
docs-root: docs/architecture
diagram: plantuml
contracts:
  sync: openapi-3.1
  async: asyncapi-2.6
```

## Learn from the repository

- [`docs/sa-learning-guide.md`](docs/sa-learning-guide.md) explains SA reasoning, inputs, outputs, and a practice path.
- [`docs/repository-layout-guide.md`](docs/repository-layout-guide.md) explains every folder and file.
- [`examples/express-lane`](examples/express-lane) contains a complete architecture brief and the specialist artifacts justified by it.

## Local development

Clone the repository and load it directly without installing it into the plugin cache:

```bash
git clone https://github.com/phubkhn/skill-sa.git
cd skill-sa
claude --plugin-dir .
```

After editing plugin files in an active session, run `/reload-plugins`.

Validate the repository before publishing:

```bash
python3 scripts/validate_repo.py
claude plugin validate .
```

## Publish a new version

The plugin manifest uses an explicit semantic version. To publish an update:

1. Update `version` in `.claude-plugin/plugin.json`.
2. Run both validation commands above.
3. Commit and push the release to the marketplace repository.
4. Test the user update flow with `claude plugin marketplace update skill-sa` followed by `claude plugin update sa@skill-sa`.

When an explicit manifest version is unchanged, Claude Code treats the cached plugin as the same release. Always bump the version when publishing user-visible changes.

## Troubleshooting

- **`/plugin` is unknown:** update Claude Code, restart it, and retry.
- **`sa@skill-sa` is not found:** run `claude plugin marketplace update skill-sa`, then install again.
- **Commands do not appear after install or update:** run `/reload-plugins` or restart Claude Code.
- **Update targets the wrong installation:** rerun `claude plugin update sa@skill-sa --scope user|project|local` with the original scope.

See the official Claude Code documentation for [installing plugins](https://code.claude.com/docs/en/discover-plugins), [marketplace management](https://code.claude.com/docs/en/plugin-marketplaces), and [local plugin development](https://code.claude.com/docs/en/plugins).

## License

MIT — see [`LICENSE`](LICENSE).
