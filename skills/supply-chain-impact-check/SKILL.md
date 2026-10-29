---
name: supply-chain-impact-check
description: Triage external supply-chain advisories and compromise reports against a repository and, when relevant, deployed artefacts. Use when asked whether a project or running workload is affected by a dependency, lockfile, build tool, CI install path, container image, runtime trust store, or other software supply-chain incident, especially for read-only impact checks across npm, Docker, Python, and GitHub Actions.
metadata:
  author: "chearmstrong"
  canonical-source: "https://github.com/chearmstrong/skills"
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
4. Check deployed artefacts when the question includes a running environment or repository evidence cannot establish its exposure.
   - Identify the account, region, environment, workload, and running image digest or runtime version; a configured tag or task definition alone may not identify what is running.
   - Trace the affected component through the effective runtime path, including sidecars, image layers, bundled versus OS certificate stores, overrides, and the client that makes the connection where relevant. For trust-store incidents, test the actual client against an incident chain and a valid control offline when safe.
   - Compare that artefact and path with the advisory. Use read-only metadata and safe offline checks; if access or provenance is missing, mark that environment unverified rather than inferring its state from current source.
5. Decide affectedness with evidence, separately for the repository and each checked environment.
   - `Affected`: the affected component or mechanism is present in a relevant execution path.
   - `Potentially affected`: evidence is incomplete, lockfiles are stale, the install or deployed runtime path is unknown, or the advisory scope is still uncertain.
   - `Not currently affected`: the relevant checked repository or runtime path excludes the affected component or execution mechanism.
   - `Not applicable`: wrong ecosystem, package, platform, or execution path.
6. Recommend proportionate mitigations.
   - Prefer smallest safe actions: pin, override, remove, update lockfile, disable risky lifecycle execution, rotate exposed credentials, rebuild artefacts, or rerun clean CI.
   - Call out when mitigation is only useful if the repo is actually exposed.
   - Separate immediate containment from follow-up hardening.
7. Report verification limits.
   - Name files checked, commands run, and evidence missing.
   - State whether network-backed commands such as registry lookups, advisory fetches, or audit commands were unavailable.

## Evidence To Collect

- Native build hooks such as `binding.gyp`, `node-gyp`, `preinstall`, `install`, `postinstall`, `prepare`, or custom build scripts.
- Package manager controls such as `ignore-scripts`, overrides, lockfile integrity hashes, frozen installs, and registry pinning.
- Artefacts that may need rebuilding: Docker images, Lambda bundles, release packages, generated clients, or cached dependencies.

## Npm-Specific Checks

- Use `package-lock.json`, `npm-shrinkwrap.json`, `pnpm-lock.yaml`, and `yarn.lock` as evidence of resolved transitive versions, not proof of what was installed. Check the effective install options, platform, and environment or deployed artefact.
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
- Do not claim a running environment is unaffected from current source, a mutable image tag, or a configured deployment alone; identify its effective artefact and execution path.
- Do not run install, build, or package scripts during triage unless the user explicitly approves the risk.
- Do not paste secret values, tokens, or private registry credentials into the response.
- Do not recommend broad dependency upgrades when a pin, override, or removal would address the exposure more safely.
- Do not treat a secondary blog post as the final source of truth when primary advisories are available.

## Output Shape

Repeat the scope, verdict, confidence, and supporting evidence for the repository and each checked environment.

```text
Scope: <repository or environment and workload>
Verdict: affected | potentially affected | not currently affected | not applicable
Confidence: high | medium | low

Advisory claim:
- <package/mechanism/date range/source summary>

Repository evidence:
- <file/path/command evidence>

Exposure path:
- <developer, CI, release, deploy, production, or none found>

Deployed evidence (when relevant):
- <environment, running artefact and effective path; or explicitly unverified>

Recommended action:
- <immediate mitigation or "none required">

Follow-up hardening:
- <optional controls, monitoring, or cleanup>

Verification limits:
- <what was not checked or could not be verified>
```

For example, current source may pin a patched collector image while production still runs an older digest. If the running image's actual TLS client accepts an incident certificate chain (with a valid control also passing), report the repository as **not currently affected** and production as **affected**, citing each artefact. If the running digest or client cannot be checked, report production as **potentially affected** and name the missing evidence.
