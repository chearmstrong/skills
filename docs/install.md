# Install Skills

The recommended route is the direct `skills` CLI install:

```bash
npx skills add chearmstrong/skills
```

This installs the skills as normal user-level skills, which is the most
predictable setup for Codex Desktop and CLI users.

## Recommended Install

The cross-agent `skills` CLI from [skills.sh](https://www.skills.sh/) can
install this repository directly from GitHub:

```bash
npx skills add chearmstrong/skills
```

To inspect available skills before installing:

```bash
npx skills add chearmstrong/skills --list
```

To install selected skills only:

```bash
npx skills add chearmstrong/skills --skill review-pr
```

Use this route when you want a portable CLI install across supported agents. It
is the primary install path for Codex users.

## Codex Plugin Support

Codex plugin/marketplace support has been removed for now because direct skill
installation is simpler and more predictable across Codex Desktop and CLI. The
skills themselves remain portable and can still be installed manually or via
`npx skills add`.

## Secondary Install Methods

Clone the repository when you want to develop skills locally or symlink/copy
individual skill directories:

```bash
git clone https://github.com/chearmstrong/skills.git
cd skills
```

Use the plugin routes below only when you specifically want plugin namespacing
or marketplace distribution on an agent surface that supports it.

## Claude Plugin Bundle

For normal Claude Code use, add this repository as a plugin marketplace and
install the bundled plugin:

```bash
claude plugin marketplace add chearmstrong/skills
claude plugin install chearmstrong-skills@chearmstrong-skills
```

That installs the plugin for future sessions. Plugin-bundled skills are
namespaced under the plugin name, such as `/chearmstrong-skills:review-pr`.

For local development or one-off testing without installing the plugin, point a
Claude Code session at the repository root:

```bash
claude --plugin-dir "$(pwd)"
```

Do not symlink the whole repository into `~/.claude/skills`; that directory is
for individual skills or skills-directory plugins, not a marketplace checkout.

## GitHub Copilot Plugin Bundle

GitHub Copilot CLI and VS Code Insiders agent plugins support plugin
marketplaces and can install this repository as a bundle.

For GitHub Copilot CLI:

```bash
copilot plugin marketplace add chearmstrong/skills
copilot plugin install chearmstrong-skills@chearmstrong-skills
```

For VS Code Insiders, enable agent plugins if required, then add
`chearmstrong/skills` to the `Chat > Plugins: Marketplaces` setting. You can
also edit `settings.json` directly:

```json
{
  "chat.plugins.marketplaces": [
    "github/copilot-plugins",
    "github/awesome-copilot",
    "chearmstrong/skills"
  ]
}
```

Use the Agent Plugins view in the Extensions panel, or search for
`@agentPlugins`, to discover and install plugins from configured marketplaces.

This uses `.github/plugin/marketplace.json` and `.github/plugin/plugin.json`.
The plugin exposes the same skill directories under `skills/`.

## Manual Install

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

OpenCode:

```bash
mkdir -p ~/.config/opencode/skills
ln -s "$(pwd)/skills/<skill-name>" ~/.config/opencode/skills/<skill-name>
```

OpenCode also discovers skills from `~/.agents/skills`, so skills installed for
Codex through the direct-install path are available to OpenCode too.

If a target directory already exists, remove or rename it before creating the
symlink.

To link every skill into the standard user-level skills directory, link each
skill folder individually:

```bash
mkdir -p ~/.agents/skills
for skill in skills/*; do
  [ -d "$skill" ] || continue
  [ -f "$skill/SKILL.md" ] || continue
  ln -s "$(pwd)/$skill" "$HOME/.agents/skills/$(basename "$skill")"
done
```

Do not symlink the parent `skills/` directory into `~/.agents/skills`; that can
create `~/.agents/skills/skills/review-pr/SKILL.md`. The expected user-level
shape is:

```text
~/.agents/skills/review-pr/SKILL.md
~/.agents/skills/bug-hunting/SKILL.md
```

## Troubleshooting

- Restart Codex Desktop after installing.
- Start a new chat or thread.
- Check that skill folders exist under `~/.agents/skills`.
- Verify each skill folder contains `SKILL.md`.
