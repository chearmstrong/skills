# Docker Supply Chain Checks

Load this reference when the advisory involves container base images, Dockerfiles, build images, registries, image layers, or runtime image artefacts.

## What To Inspect

- `Dockerfile`, `Dockerfile.*`, `docker-compose.yml`, `.devcontainer/`, image bake files, and CI image build steps.
- Base image references, including registry, tag, digest, and stage aliases.
- Package-manager commands inside image builds: `apt`, `apk`, `yum`, `dnf`, `pip`, `npm`, `curl | sh`, downloaded binaries, and copied artefacts from previous stages.
- Build arguments and secrets used during image builds. Report secret presence without revealing values.
- Registry paths and release workflows that publish or promote images.

## Docker-Specific Judgement

- A tag match is not enough to prove affectedness; mutable tags can move. Prefer digests, build timestamps, SBOMs, provenance, or registry metadata when available.
- A vulnerable build-stage package matters if its artefacts are copied into the final image, even when the final stage does not contain the package manager.
- A vulnerable final-stage package matters at runtime even if application lockfiles are clean.
- A compromised build image can contaminate generated artefacts, compiled binaries, or vendored dependencies copied into later stages.
- Cached layers can preserve exposure after source files are updated; note when a clean rebuild and republish is required.

## Mitigation Patterns

- Pin or update base image digests when the base image is in scope.
- Rebuild from a clean cache after replacing compromised build inputs.
- Rebuild and republish downstream images that copied artefacts from affected stages.
- Rotate build-time credentials if a compromised build step could read them.
- Prefer narrow package updates over broad image refreshes unless the base image or OS layer is the affected component.

## Do Not

- Do not call a project safe just because application manifests are clean; Dockerfiles can install additional packages.
- Do not assume `latest`, distro tags, or language runtime tags are stable evidence.
- Do not recommend only dependency lockfile changes when the exposure is in an image layer or build stage.
