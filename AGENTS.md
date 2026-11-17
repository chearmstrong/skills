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
- Every published skill must declare `author: "chearmstrong"` and
  `canonical-source: "https://github.com/chearmstrong/skills"` under
  `metadata`.
- Keep long reference material in `references/`, repeatable helpers in
  `scripts/`, and static templates in `assets/`.
- Keep product-specific files optional; a skill should still make sense to an
  agent that only reads `SKILL.md`.

## Companion Skills

- When naming a companion skill as guidance, link directly to its published
  `SKILL.md`. Prefer installed guidance; allow optional web consultation and
  state how to continue when neither source is accessible.
- Read supporting references only when relevant to the task. Keep companion
  guidance optional unless the workflow requires it.
- When adding or changing a companion reference, verify that the link points
  to the intended published skill. Report any verification limitation.
- When renaming or removing a skill, update affected companion references,
  links, README entries, and manifests in the same change.

## Plugin Metadata

- `.claude-plugin/plugin.json` is the Claude plugin manifest for the same
  repository-level skill bundle.
- `.github/plugin/marketplace.json` is the GitHub Copilot CLI marketplace
  manifest, and `.github/plugin/plugin.json` is the GitHub Copilot CLI plugin
  manifest.
- Codex plugin/marketplace support has been removed. Prefer documenting
  `npx skills add chearmstrong/skills` for Codex Desktop and CLI users.
- Keep plugin manifests aligned with `skills/` whenever a skill is added,
  removed, or renamed.
- `CLAUDE.md` should remain a symlink to `AGENTS.md` so repository instructions
  stay single-sourced.

## Editing Rules

- Make small, focused changes.
- Match the existing Markdown style.
- Avoid broad refactors, reformatting, or unrelated cleanup.
- Use relative links for resources bundled with the skill and repository
  documentation; use published URLs for companion skills that may be installed
  separately.
- If generated tables or manifests change, update only the affected entries.

## Verification

Before claiming changes are ready:

- Run `./scripts/validate-skills.sh skills/<name>` for each changed skill;
  run `./scripts/validate-skills.sh` for bundle-wide changes.
- Check `git diff --check`.
- Review the diff for portability, stale manifest entries, and accidental
  product-specific assumptions.
