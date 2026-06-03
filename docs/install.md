# Install Skills

Clone the repository:

```bash
git clone https://github.com/chearmstrong/skills.git
cd skills
```

Use the plugin bundle when you want the skills namespaced and distributed
together. Install individual skills when you want the simplest direct setup or
when using an agent surface that does not support plugin marketplaces.

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

## Codex Plugin Bundle

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

## Direct Skill Install

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
