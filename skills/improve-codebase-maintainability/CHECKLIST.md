# Maintainability Review Checklist

Use this optional broad-scan checklist only when `SKILL.md` says to load it.
For targeted refactors or already-obvious hotspots, keep the review in
`SKILL.md` and do not load this file.

## Code quality

- Are functions short enough to understand without scrolling?
- Is branching shallow and easy to follow?
- Are names specific to the domain?
- Are side effects obvious?
- Are errors handled consistently?
- Is the code mixing multiple abstraction levels?

## Duplication

Look for repeated:

- Validation
- Mapping
- Formatting
- Error handling
- Config parsing
- Permission checks
- AWS client creation
- Logging
- Test setup
- Constants/magic strings

Before extracting, ask:

- Will these call sites evolve together?
- Can the helper have a clear name?
- Will the abstraction reduce cognitive load?
- Would adding options/flags make it worse?
- Is this business-rule duplication or just similar syntax?

## Large files

A large file is a problem when it contains multiple responsibilities.

Good split signals:

- One section changes independently from another
- Helpers serve only part of the file
- Tests are hard to target
- The file mixes handler/controller, domain, and infrastructure code
- Naming sections would reveal separate modules

Avoid splitting:

- Generated files
- Snapshots
- Migrations
- Simple declarative config
- Files that are long but cohesive

## Test safety

Before refactoring:

- Identify existing tests
- Add characterization tests if needed
- Prefer testing observable behaviour
- Avoid tests that lock in private implementation details

## Type safety

Check for:

- `any`
- untyped config/env
- nullable fields used unsafely
- stringly-typed states
- weak return types
- repeated shape checks that could be centralised

## Weak interfaces

Check for modules where callers must know too much:

- repeated sequencing of the same helper calls
- option bags or boolean flags exposing unrelated internal branches
- public functions that require callers to pass intermediate state
- domain rules split across several call sites
- tests coupled to private helpers instead of observable behaviour

Prefer a deeper interface only when it improves locality, reduces repeated
orchestration, or makes behaviour easier to test.

## Backend/AWS checks

Check for:

- direct env var access scattered across files
- inconsistent logging
- unsafe logging of sensitive values
- repeated AWS SDK clients
- missing retry/timeout/idempotency handling
- handlers that contain too much domain logic
- infrastructure concerns leaking into domain logic
