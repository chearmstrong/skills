# Agent Skills

Portable personal coding-agent skills shared from `~/.agents`.

These skills are maintained as normal skill directories and can be copied or
symlinked into compatible agent skill folders.

## Install

Clone the repository:

```bash
git clone https://github.com/chearmstrong/skills.git
cd skills
```

This repository contains:

- individual portable skills under `skills/`
- a Claude plugin bundle at the repository root, described by `.claude-plugin/`
- a Codex marketplace at `.agents/plugins/marketplace.json`, pointing to the
  Codex plugin package under `skills/`

Use the plugin bundle when you want the skills namespaced and distributed
together. Install individual skills when you want the simplest setup or Copilot
support.

| Goal | Agents | Method |
| --- | --- | --- |
| Use the whole bundle | Claude Code | Point Claude at this checkout with `--plugin-dir`. |
| Use the whole bundle | Codex | Add this checkout through a Codex marketplace entry. |
| Use selected skills | Codex, Claude Code, Copilot | Symlink or copy individual directories from `skills/`. |

### Claude Plugin Bundle

For a local Claude Code session, point Claude at the repository root:

```bash
claude --plugin-dir "$(pwd)"
```

Plugin-bundled skills are namespaced under the plugin name, such as
`/chearmstrong-skills:review-pr`.

Do not symlink the whole repository into `~/.claude/skills`; that directory is
for individual skills.

### Codex Plugin Bundle

The `skills/.codex-plugin/plugin.json` file describes the Codex plugin bundle.
Codex discovers local plugins through marketplaces, so this repository includes
a marketplace file that points to `skills/`.

To add this repository as a Codex marketplace from the Codex app:

- Source: `chearmstrong/skills`
- Git ref: `main`
- Sparse paths: leave blank

For the CLI equivalent:

```bash
codex plugin marketplace add chearmstrong/skills --ref main
```

For local personal use, direct skill install is usually simpler. Use the Codex
plugin route when you want plugin namespacing, marketplace distribution, or
workspace sharing.

### Direct Skill Install

Symlink or copy the individual skill directories you want. Replace
`<skill-name>` with a directory under `skills/`.

Codex:

```bash
mkdir -p ~/.agents/skills
ln -s "$(pwd)/skills/<skill-name>" ~/.agents/skills/<skill-name>
```

Claude Code:

```bash
mkdir -p ~/.claude/skills
ln -s "$(pwd)/skills/<skill-name>" ~/.claude/skills/<skill-name>
```

GitHub Copilot:

```bash
mkdir -p ~/.copilot/skills
ln -s "$(pwd)/skills/<skill-name>" ~/.copilot/skills/<skill-name>
```

If a target directory already exists, remove or rename it before creating the
symlink.

## Documentation

- [Codex skills](https://developers.openai.com/codex/skills)
- [Codex plugins](https://developers.openai.com/codex/plugins)
- [Build Codex plugins](https://developers.openai.com/codex/plugins/build)
- [Claude Code skills](https://code.claude.com/docs/en/skills)
- [Claude Code plugins](https://code.claude.com/docs/en/plugins)
- [Claude Code plugin marketplaces](https://code.claude.com/docs/en/plugin-marketplaces)
- [Claude Code memory and CLAUDE.md](https://code.claude.com/docs/en/memory)
- [GitHub Copilot agent skills](https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/customize-cloud-agent/add-skills)
- [GitHub Copilot customisation cheat sheet](https://docs.github.com/en/copilot/reference/customization-cheat-sheet)

`CLAUDE.md` is intentionally a symlink to `AGENTS.md` so agent instructions stay
single-sourced.

## Skills

<!-- skills-table:start -->
| Skill | Description |
| --- | --- |
| `architecture-compliance-check` | Verify architecture and implementation follow documented best practices, project patterns, and user rules. Check against project documentation, ensure no assumptions are made, and verify implementation matches documented patterns. Use when reviewing code, implementing features, making architectural decisions, or before committing changes. |
| `commit-message` | Generate a Conventional Commits message from uncommitted changes. Use when the user asks for a commit message, conventional commit, or summary of staged and unstaged changes without committing. |
| `documentation-review` | Review documentation to ensure it matches implementation, is correct and up-to-date, clear and concise, uses British English, and has no duplication or redundancy. Works with or without MCP; prefers Context7 / AWS docs MCP when enabled, otherwise web search and official docs. Use when reviewing documentation files, code comments, docstrings, or when documentation may be outdated. Applies to markdown files, README files, code comments, and docstrings. |
| `execute-plan-with-gates` | Use only when the user explicitly asks to execute an implementation plan with gated or ungated phase controls, including whether to pause between phases, ask before commits, and ask before moving to the next phase. Do not use for generic plan execution unless the user mentions gates, gated mode, ungated mode, approvals, phase checkpoints, or commit permission. |
| `gh-address-copilot-comments` | Inspect, fix, and resolve GitHub Copilot automated pull request review comments. Use when the user asks to check, triage, fix, reply to, address, or resolve Copilot PR review comments, especially unresolved inline review threads that require GitHub GraphQL via the GitHub CLI. |
| `improve-codebase-maintainability` | Review a codebase for practical maintainability improvements: overly complex code, duplicated logic, large files, weak abstractions, unclear naming, poor locality, and refactoring opportunities. Use when the user wants to improve code quality without changing behaviour. |
| `manual-review-comment-export` | Use only when the user explicitly invokes this manual skill or asks for review feedback exported in the `- path:line` plus quoted-comment format for the review-comments skill. Do not use for ordinary code review, PR review, self-review, or completion checks unless this exact manual export format is requested. |
| `review-comments` | Address PR or code review comments. Use when given review comments to verify before fixing, research best practices with available documentation tools or official sources, and document whether each comment was valid, partially valid, or invalid. |
| `review-pr` | Review a colleague's pull request or branch diff read-only. Use only when the user is reviewing someone else's PR, a PR URL/number, or another author's branch, and wants draft review comments without editing code. |
<!-- skills-table:end -->

## Notes

- `SKILL.md` is the portable source of truth for each skill.
- `skills/` is also the Codex plugin package, so plugin installs and direct
  skill installs use the same source files.
- Optional helper scripts live inside each skill's `scripts/` directory.
- Product-specific metadata is optional and should not be required to use a skill.
