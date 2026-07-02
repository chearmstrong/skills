# Agent Skills

[![skills.sh](https://skills.sh/b/chearmstrong/skills)](https://skills.sh/chearmstrong/skills)

Portable personal coding-agent skills shared from `~/.agents`.

These skills are maintained as normal skill directories and can be installed,
copied, or symlinked into compatible agent skill folders.

## Recommended Install

```bash
npx skills add chearmstrong/skills
```

This installs the skills as normal user-level skills, which is the most
predictable setup for Codex Desktop and CLI users.

To install one selected skill:

```bash
npx skills add chearmstrong/skills --skill review-pr
```

## Repository Contents

- Individual portable skills under `skills/`.
- A Claude plugin bundle and marketplace at the repository root, described by
  `.claude-plugin/`.
- A GitHub Copilot agent plugin bundle and marketplace, described by
  `.github/plugin/`.

Use `npx skills add chearmstrong/skills` for the default direct install. Plugin
bundles remain secondary routes for agent surfaces that already support them.

Codex plugin/marketplace support has been removed for now because direct skill
installation is simpler and more predictable across Codex Desktop and CLI. The
skills themselves remain portable and can still be installed manually or via
`npx skills add`.

| Goal                 | Agents                                    | Method                                                                          |
| -------------------- | ----------------------------------------- | ------------------------------------------------------------------------------- |
| Use the whole bundle | Codex, Claude Code, Copilot CLI, OpenCode | Install through `skills.sh` with `npx skills add chearmstrong/skills`.          |
| Use selected skills  | Codex, Claude Code, Copilot CLI, OpenCode | Install through `skills.sh` with `npx skills add chearmstrong/skills --skill review-pr`. |
| Use plugin bundle    | Claude Code                               | Add this checkout as a Claude marketplace, then install `chearmstrong-skills`.  |
| Use plugin bundle    | GitHub Copilot CLI, VS Code Insiders      | Add this checkout as a Copilot marketplace, then install `chearmstrong-skills`. |
| Use selected skills  | Codex, Claude Code, Copilot CLI, OpenCode | Symlink or copy individual directories from `skills/`.                          |

## Skills

<!-- skills-table:start -->

| Skill                                                   | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| ------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [`architecture-compliance-check`](skills/architecture-compliance-check)       | Verify architecture and implementation follow documented best practices, project patterns, and user rules. Check against project documentation, ensure no assumptions are made, and verify implementation matches documented patterns. Use when reviewing code, implementing features, making architectural decisions, or before committing changes.                                                                                                                   |
| [`bug-hunting`](skills/bug-hunting)                                   | Use when asked to find bugs, audit an existing repository or scoped path, review a branch or pull request for correctness, investigate a suspected defect, or assess security/data-integrity risks without making speculative findings.                                                                                                                                                                                                                             |
| [`commit-message`](skills/commit-message)                                 | Generate a Conventional Commits message from uncommitted changes. Use when the user asks for a commit message, conventional commit, or summary of staged and unstaged changes without committing.                                                                                                                                                                                                                                                                      |
| [`cost-to-serve-estimator`](skills/cost-to-serve-estimator)                 | Estimate and document cost-to-serve for cloud-hosted AI, LLM, AWS Bedrock, agent workflow, serverless, container, or SaaS control-plane systems. Use when the user asks for rough or granular service run-rate costs, infrastructure baseline estimates, sponsorship estimates, squad/team scaling projections, AWS cost breakdowns, Bedrock model cost analysis, or reusable documentation of cost assumptions.                                                     |
| [`documentation-review`](skills/documentation-review)                       | Review documentation to ensure it matches implementation, is correct and up-to-date, clear and concise, follows the appropriate language or locale variant, and has no duplication or redundancy. Works with or without MCP; prefers Context7 / AWS docs MCP when enabled, otherwise web search and official docs. Use when reviewing documentation files, code comments, docstrings, or when documentation may be outdated. Applies to markdown files, README files, code comments, and docstrings. |
| [`dynamodb-guardrails`](skills/dynamodb-guardrails)                         | Use when adding, changing, debugging, or reviewing DynamoDB code, schemas, CDK/IaC, pagination, queries, scans, indexes, writes, retries, or tests. Ensures AWS-backed best practices, identifies anti-patterns, and proposes minimal safe fixes for DynamoDB usage.                                                                                                                                     |
| [`execute-plan-with-gates`](skills/execute-plan-with-gates)                 | Use only when the user explicitly asks to execute an implementation plan with gated or ungated phase controls, including whether to pause between phases, ask before commits, and ask before moving to the next phase. Do not use for generic plan execution unless the user mentions gates, gated mode, ungated mode, approvals, phase checkpoints, or commit permission.                                                                                             |
| [`gh-address-copilot-comments`](skills/gh-address-copilot-comments)         | Inspect, fix, and resolve GitHub Copilot automated pull request review comments. Use when the user asks to check, triage, fix, reply to, address, or resolve Copilot PR review comments, especially unresolved inline review threads that require GitHub GraphQL via the GitHub CLI.                                                                                                                                                                                   |
| [`governance-eval-designer`](skills/governance-eval-designer)               | Use when designing or reviewing AI workflow governance: audit fields, decision traces, approval gates, pause or stop rules, rollout widen gates, offline evals, golden datasets, eval harnesses, structured-output validators, or repo-aware governance templates for agents, RAG/docs assistants, support assistants, coding agents, and approval-gated automations.                                                                                                  |
| [`improve-codebase-maintainability`](skills/improve-codebase-maintainability) | Review a codebase for practical maintainability improvements: overly complex code, duplicated logic, large files, weak abstractions, unclear naming, poor locality, and refactoring opportunities. Use when the user wants to improve code quality without changing behaviour.                                                                                                                                                                                         |
| [`lambda-guardrails`](skills/lambda-guardrails)                             | Use when adding, changing, debugging, or reviewing AWS Lambda functions, handlers, event sources, async invocations, retries, timeouts, concurrency, IAM permissions, environment variables, VPC access, packaging, observability, or Lambda CDK/IaC. Ensures AWS-backed best practices, identifies Lambda anti-patterns, and proposes minimal safe fixes.                                               |
| [`manual-review-comment-export`](skills/manual-review-comment-export)       | Use only when the user explicitly invokes this manual skill or asks for review feedback exported in the `- path:line` plus quoted-comment format for the review-comments skill. Do not use for ordinary code review, PR review, self-review, or completion checks unless this exact manual export format is requested.                                                                                                                                                 |
| [`review-comments`](skills/review-comments)                                 | Address PR or code review comments. Use when given review comments to verify before fixing, research best practices with available documentation tools or official sources, and document whether each comment was valid, partially valid, or invalid.                                                                                                                                                                                                                  |
| [`review-pr`](skills/review-pr)                                             | Review a colleague's pull request or branch diff read-only. Use only when the user is reviewing someone else's PR, a PR URL/number, or another author's branch, and wants draft review comments without editing code.                                                                                                                                                                                                                                                  |
| [`slack-ui-ux`](skills/slack-ui-ux)                                         | Design, review, or improve generic Slack app user experiences, Slack UI/UX, Block Kit messages, modals, App Home views, shortcuts, buttons, select menus, approval flows, Assistant-style Slack interactions, Slack-facing copy, and interaction safety. Use when changing Slack surfaces or Slack product behaviour; verify against official Slack documentation for Block Kit limits, modals, interactivity, Events API retries, OAuth scopes, Web API methods, rate limits, manifests, or newly released Slack platform features. |
| [`supply-chain-impact-check`](skills/supply-chain-impact-check)             | Triage external supply-chain advisories and compromise reports against a local repository. Use when asked whether a project is affected by an npm, package manager, build tool, dependency, lockfile, CI install path, native build hook, or software supply-chain incident, especially for read-only impact checks and mitigation recommendations across npm, Docker, Python, GitHub Actions, and public advisory sources.                                          |
| [`technical-writing`](skills/technical-writing)                             | Use when reviewing, planning, editing, or drafting technical writing such as documentation, blog posts, READMEs, ADRs, release notes, tutorials, how-to guides, reference material, explanations, public engineering posts, or publication-safe technical content.                                                                          |
| [`tool-vs-mcp-boundary-review`](skills/tool-vs-mcp-boundary-review)         | Use when deciding whether an AI assistant capability should be an inline helper, an agent-callable tool, a separate MCP-style server or tool boundary, or blocked from v1 because of trust, permissions, audit, ownership, blast radius, sensitive data, side effects, cost, or reuse concerns.                                                                                                             |

<!-- skills-table:end -->

## Install

Clone the repository:

```bash
git clone https://github.com/chearmstrong/skills.git
cd skills
```

See [Install Skills](docs/install.md) for `skills.sh`, secondary plugin routes,
and manual install instructions.

## Validate Skills

Validate every skill directory in this repository:

```bash
./scripts/validate-skills.sh
```

Validate one skill directory:

```bash
./scripts/validate-skills.sh skills/review-pr
```

The script validates individual skill roots because `skills/` is a bundle
directory, not a skill directory with its own `SKILL.md`.

If npm registry access is unavailable, the script falls back to the local
portable validator when it exists at
`~/.agents/skills/skill-maintenance/scripts/validate_skills.py`. Set
`SKILLS_FALLBACK_VALIDATOR` to use a different fallback validator path.

## More Documentation

- [Install Skills](docs/install.md)
- [Working Style](docs/working-style.md)
- [Resources](docs/resources.md)

## Notes

- `SKILL.md` is the portable source of truth for each skill.
- Optional helper scripts live inside each skill's `scripts/` directory.
- Product-specific metadata is optional and should not be required to use a skill.
- `CLAUDE.md` is intentionally a symlink to `AGENTS.md` so agent instructions
  stay single-sourced.
