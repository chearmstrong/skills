# Python Supply Chain Checks

Load this reference when the advisory involves Python packages, package indexes, wheels, native extensions, virtual environments, or Python build tooling.

## What To Inspect

- `pyproject.toml`, `requirements*.txt`, `constraints*.txt`, `Pipfile.lock`, `poetry.lock`, `uv.lock`, `setup.py`, `setup.cfg`, and workspace/package directories.
- CI, Docker, Makefile, tox, nox, Hatch, Poetry, uv, pip-tools, and release build commands.
- Package indexes and authentication: `pip.conf`, environment docs, private index URLs, trusted-host settings, and publish workflows.
- Native build paths: source distributions, wheels, C/C++/Rust extensions, `auditwheel`, `maturin`, `setuptools`, and compiler toolchains.

## Python-Specific Judgement

- Lockfile absence lowers confidence; manifests alone often do not prove the transitive installed version.
- Wheels can avoid local native builds, but a compromised wheel is still executable code. Source distributions can execute build backends during installation.
- Dev/test-only dependencies can still affect CI, release artefacts, generated clients, or build outputs.
- Multiple Python environments may exist in one repo; check app, tooling, docs, and deployment folders separately.
- Private index fallback behaviour matters. A dependency-confusion risk can exist even when the named package is internal.

## Mitigation Patterns

- Pin or constrain the affected package and regenerate the lockfile with the repo's package manager.
- Prefer hashes or lockfile integrity controls where the repo already supports them.
- Rebuild wheels, containers, Lambda bundles, or generated artefacts created during the affected window.
- Rotate package index tokens if compromised install/build steps could read them.
- Separate immediate containment from longer-term hardening such as hash checking, private-index precedence, or build isolation.

## Do Not

- Do not rely on `pip freeze` unless it was captured from the exact environment in question.
- Do not treat a clean top-level `requirements.txt` as proof when constraints, extras, or lockfiles install transitives.
- Do not run install/build commands during triage without approval; Python build backends can execute code.
