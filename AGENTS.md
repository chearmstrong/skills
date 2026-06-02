# Agent Instructions

## Repository Purpose

This repository publishes portable coding-agent skills. Keep each skill usable
from a plain `SKILL.md` directory, then add product-specific metadata only when
it improves discovery or installation.

## Language

Use British English in documentation and new prose. Preserve existing spelling
when quoting APIs, logs, external text, or identifiers.

## Skill Maintenance

- Treat each directory under `skills/` as an Agent Skill.
- Keep `SKILL.md` as the portable source of truth.
- Use only the required `name` and `description` frontmatter by default.
- Add optional frontmatter only when it is part of the Agent Skills
  specification and has clear value.
- Keep long reference material in `references/`, repeatable helpers in
  `scripts/`, and static templates in `assets/`.
- Keep product-specific files optional; a skill should still make sense to an
  agent that only reads `SKILL.md`.
- Do not rename existing skill directories without updating every manifest and
  README reference in the same change.

## Plugin Metadata

- `.agents/plugins/marketplace.json` is the Codex marketplace manifest.
- `plugins/chearmstrong-skills/.codex-plugin/plugin.json` is the Codex plugin
  manifest and should expose the wrapper's `skills/` directory as the source of
  skills.
- `.claude-plugin/plugin.json` is the Claude plugin manifest for the same
  repository-level skill bundle.
- Keep plugin manifests aligned with `skills/` whenever a skill is added,
  removed, or renamed.
- Keep `plugins/chearmstrong-skills/skills/` aligned with `skills/`; Codex
  packages the wrapper directory rather than following a symlink to the root
  skills directory.
- `CLAUDE.md` should remain a symlink to `AGENTS.md` so repository instructions
  stay single-sourced.

## Editing Rules

- Make small, focused changes.
- Match the existing Markdown style.
- Avoid broad refactors, reformatting, or unrelated cleanup.
- Prefer relative links in repository documentation.
- If generated tables or manifests change, update only the affected entries.

## Verification

Before claiming changes are ready:

- Run the available skill validation command if one exists in the environment.
- Check `git diff --check`.
- Review the diff for portability, stale manifest entries, and accidental
  product-specific assumptions.
