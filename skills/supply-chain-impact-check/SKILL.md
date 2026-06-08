---
name: supply-chain-impact-check
description: Triage external supply-chain advisories and compromise reports against a local repository. Use when asked whether a project is affected by an npm, package manager, build tool, dependency, lockfile, CI install path, native build hook, or software supply-chain incident, especially for read-only impact checks and mitigation recommendations across npm, Docker, Python, GitHub Actions, and public advisory sources.
---

# Supply Chain Impact Check

Use this skill to answer "are we affected?" for a published or reported supply-chain issue. The goal is a defensible impact assessment, not a generic security summary.

Default to read-only work. Do not change dependencies, lockfiles, CI workflows, secrets, or repository configuration unless the user explicitly asks for remediation after the assessment.

## Workflow

1. Establish the advisory claim.
   - Identify the package, ecosystem, affected versions, compromise mechanism, entry point, and claimed date range.
   - Prefer primary sources: maintainer advisories, registry notices, CVEs/GHSAs, official incident write-ups, and source diffs.
   - Load `references/advisory-sources.md` when the user provides only a blog post, news article, social post, vague package name, or unstructured incident report.
   - If using a secondary article, separate what the article claims from what the repository evidence proves.
2. Check direct and transitive exposure.
   - Inspect package manifests, lockfiles, workspaces, package manager config, and build tooling.
   - For npm projects, check `package.json`, lockfiles, `.npmrc`, workspace manifests, lifecycle scripts, native addon dependencies, and package manager overrides.
   - Look for aliases, bundled dependencies, vendored copies, generated lockfile sections, and multiple package managers.
3. Trace install and build execution paths.
   - Inspect CI workflows, Dockerfiles, devcontainer files, Makefiles, Justfiles, release workflows, and deployment build scripts.
   - Identify whether install commands run lifecycle scripts, native builds, or arbitrary package scripts.
   - Distinguish developer-only exposure from CI, release, deploy, production image, and runtime exposure.
   - If Docker images, Python packages, or GitHub Actions are in scope, load only the relevant reference from `references/`.
4. Decide affectedness with evidence.
   - `Affected`: vulnerable or compromised package/version is installed or executable in a relevant path.
   - `Potentially affected`: evidence is incomplete, lockfiles are stale, install path is dynamic, or the advisory scope is still uncertain.
   - `Not currently affected`: manifests/lockfiles/build paths do not include the affected package or execution mechanism.
   - `Not applicable`: wrong ecosystem, package, platform, or execution path.
5. Recommend proportionate mitigations.
   - Prefer smallest safe actions: pin, override, remove, update lockfile, disable risky lifecycle execution, rotate exposed credentials, rebuild artefacts, or rerun clean CI.
   - Call out when mitigation is only useful if the repo is actually exposed.
   - Separate immediate containment from follow-up hardening.
6. Report verification limits.
   - Name files checked, commands run, and evidence missing.
   - State whether network-backed commands such as registry lookups, advisory fetches, or audit commands were unavailable.

## Evidence To Collect

- Package names, versions, and lockfile entries.
- Install commands and whether lifecycle scripts run.
- CI/release/deploy paths that execute dependency installation.
- Native build hooks such as `binding.gyp`, `node-gyp`, `preinstall`, `install`, `postinstall`, `prepare`, or custom build scripts.
- Package manager controls such as `ignore-scripts`, overrides, lockfile integrity hashes, frozen installs, and registry pinning.
- Artefacts that may need rebuilding: Docker images, Lambda bundles, release packages, generated clients, or cached dependencies.

## Npm-Specific Checks

- Treat `package-lock.json`, `npm-shrinkwrap.json`, `pnpm-lock.yaml`, and `yarn.lock` as the source of installed transitive versions.
- Check every workspace package, not only the repository root.
- `npm ci` installs from the lockfile but still runs lifecycle scripts unless configured otherwise.
- `npm audit` may miss active compromise reports before advisory databases update; do not rely on it alone.
- A package can be risky even if it is dev-only when CI, release, or Docker builds execute it.

## Ecosystem References

Load these only when the repository or advisory touches that ecosystem:

- `references/docker.md`: Docker base images, image rebuilds, multi-stage builds, registries, and runtime image exposure.
- `references/python.md`: Python package exposure, lockfiles, virtual environments, wheels, native extensions, and package indexes.
- `references/github-actions.md`: GitHub Actions workflow, action pinning, runner, token, cache, and artifact exposure.
- `references/advisory-sources.md`: open structured sources for advisory details, affected versions, aliases, and malicious package reports.

Do not load every reference by default. Pick the smallest set needed to answer the affectedness question.

## Guardrails

- Do not claim "safe" from manifest absence alone when lockfiles, workspaces, or generated dependency trees exist.
- Do not claim "affected" from a package-name match alone; verify version, path, and execution mechanism.
- Do not run install, build, or package scripts during triage unless the user explicitly approves the risk.
- Do not paste secret values, tokens, or private registry credentials into the response.
- Do not recommend broad dependency upgrades when a pin, override, or removal would address the exposure more safely.
- Do not treat a secondary blog post as the final source of truth when primary advisories are available.

## Output Shape

```text
Verdict: affected | potentially affected | not currently affected | not applicable
Confidence: high | medium | low

Advisory claim:
- <package/mechanism/date range/source summary>

Repository evidence:
- <file/path/command evidence>

Exposure path:
- <developer, CI, release, deploy, production, or none found>

Recommended action:
- <immediate mitigation or "none required">

Follow-up hardening:
- <optional controls, monitoring, or cleanup>

Verification limits:
- <what was not checked or could not be verified>
```
