# GitHub Actions Supply Chain Checks

Load this reference when the advisory involves GitHub Actions, workflow dependencies, CI runners, caches, artifacts, tokens, or action maintainers.

## What To Inspect

- `.github/workflows/*.yml`, reusable workflows, composite actions, local actions, and action references in nested repositories.
- Third-party `uses:` references, whether they are pinned to SHA, tag, or branch.
- Workflow triggers: `pull_request`, `pull_request_target`, `workflow_run`, `schedule`, release, tag, and manual dispatch.
- Permissions blocks, token scopes, secret access, environment protections, and runner labels.
- Cache keys, restored paths, uploaded artifacts, downloaded artifacts, and release assets.

## GitHub-Actions-Specific Judgement

- Tag-pinned actions are mutable; SHA pinning gives stronger evidence.
- `pull_request_target` can expose privileged tokens to untrusted code if checkout and execution are not separated carefully.
- Compromised actions can read tokens, secrets, workspace contents, caches, and generated artefacts available to that job.
- Self-hosted runners can persist state between jobs; hosted runners normally reduce persistence but do not eliminate token/artifact exposure.
- A compromised CI action may require rotating tokens even when application dependencies are unaffected.

## Mitigation Patterns

- Pin third-party actions to SHAs or update to a known-good SHA.
- Reduce `GITHUB_TOKEN` permissions and job-level secret exposure.
- Invalidate caches and artifacts if a compromised workflow could have written or read them.
- Rotate repository, organisation, cloud, package registry, and app credentials exposed to affected jobs.
- Re-run release or deployment workflows from clean commits after replacing compromised actions.

## Do Not

- Do not call a repo safe because package lockfiles are clean when the advisory is about CI actions.
- Do not assume Dependabot or GitHub alerts cover action compromise immediately.
- Do not recommend rotating every secret by default; tie rotation to jobs where the compromised action had access.
