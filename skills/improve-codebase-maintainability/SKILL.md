---
name: improve-codebase-maintainability
description: "Review a codebase for practical maintainability improvements: overly complex code, duplicated logic, large files, weak abstractions, unclear naming, poor locality, and refactoring opportunities. Use when the user wants to improve code quality without changing behaviour."
---

# Improve Codebase Maintainability

Find practical, low-risk opportunities to improve the codebase without changing behaviour.

The goal is not to redesign the whole system. The goal is to make the codebase easier to read, safer to change, easier to test, and less repetitive.

Focus on:

- Code quality and readability
- Overly complex or hard-to-follow code
- Duplicated logic across files
- Large files doing too many things
- Poor separation of concerns
- Repeated validation, mapping, parsing, formatting, or error-handling logic
- Brittle tests or missing tests around risky areas
- Refactors that improve locality and reduce cognitive load
- Interfaces that leak sequencing, invariants, or implementation details to callers

Avoid speculative architecture rewrites.

## Progressive Disclosure

Use this `SKILL.md` for the judgement framework, candidate format, and implementation workflow.

Load [`CHECKLIST.md`](CHECKLIST.md) only when:

- The user asks for a broad maintainability review of a whole repository or large module.
- The codebase is unfamiliar and you need a scan checklist to avoid missing common hotspot types.
- You need category-specific prompts for duplication, large files, test safety, types, or backend/AWS maintainability.

Do not load `CHECKLIST.md` when:

- The user already named a specific file, module, or refactor candidate.
- You are implementing a previously selected candidate.
- The repository is small enough that the relevant hotspot is already obvious from the request.

## Vocabulary

Use these terms consistently:

- **Hotspot** — an area of code that is hard to understand, hard to change, duplicated, too large, or likely to cause bugs.
- **Duplication** — repeated logic, structure, or behaviour that could be extracted safely.
- **Locality** — how close related logic is to the code that uses it.
- **Cognitive load** — how much context a maintainer must hold to understand or change the code.
- **Interface** — everything a caller must know to use a module correctly: the public functions/types plus ordering, invariants, error modes, configuration, and performance expectations.
- **Deep module** — a module with a small interface that hides useful complexity and gives callers leverage.
- **Shallow module** — a module whose interface is nearly as complex as its implementation, so callers still need to understand too much.
- **Refactor candidate** — a concrete, behaviour-preserving improvement.
- **Shared utility** — a reusable helper/function/module that removes duplication without hiding important domain meaning.
- **Extraction** — moving logic into a smaller function/module/file to improve readability or reuse.
- **Split** — breaking a large file/module into focused pieces.
- **Guardrail** — a test, type, lint rule, or check that makes the refactor safer.

## Core Principles

### 1. Behaviour must not change

Every recommendation should be behaviour-preserving unless the user explicitly asks otherwise.

Before suggesting implementation changes, identify how behaviour will be protected:

- Existing tests
- New characterization tests
- Type checks
- Snapshot/golden tests where appropriate
- Manual verification steps
- Build/lint/test commands

### 2. Prefer small, reviewable refactors

Prefer changes that can be reviewed in a single PR.

Avoid “big bang” rewrites. If an improvement is large, split it into staged refactors.

Good staged shape:

1. Add or improve tests around existing behaviour.
2. Extract duplicated logic.
3. Simplify call sites.
4. Remove dead or redundant code.
5. Tighten naming/types once behaviour is protected.

### 3. Do not over-abstract

Duplication is not always bad.

Do not extract shared utilities when:

- The duplicated code is likely to evolve differently.
- The extracted helper would need lots of flags/options.
- The helper name would be vague.
- The abstraction hides important domain behaviour.
- Only two tiny call sites would become harder to read.

Prefer duplication over the wrong abstraction.

### 4. Improve locality

A good refactor should make future changes happen in fewer places.

Look for logic that is spread across handlers, controllers, routes, jobs, tests, or UI components but belongs together.

Examples:

- Repeated request validation
- Repeated response shaping
- Repeated date/currency/string formatting
- Repeated error mapping
- Repeated AWS SDK client setup
- Repeated environment/config parsing
- Repeated permission checks
- Repeated retry/backoff logic
- Repeated test fixture setup

### 5. Respect existing project conventions

Before making recommendations, inspect:

- README and contributing docs
- Existing architecture docs and ADRs
- Package scripts
- Lint/format config
- Test framework
- TypeScript/Python config
- Folder structure
- Existing utilities/helpers
- Naming conventions
- Existing patterns for errors, logging, config, and tests

Do not introduce a new style if the repo already has a clear convention.

### 6. Use interface depth as one lens

Do not turn the review into an architecture redesign. Use deep/shallow module language only when it explains a practical maintainability problem.

Look for places where callers must know too much:

- The correct sequence of helper calls
- Business invariants that are enforced at call sites
- Implementation details exposed through parameters or return shapes
- Tests that must mock or assert many internal steps instead of public outcomes
- Similar orchestration repeated across handlers, jobs, components, or tests

A good recommendation should move knowledge to the smallest sensible owner. Prefer one clear interface that preserves behaviour over many tiny helpers that force every caller to coordinate the work.

## Process

### 1. Explore the repo

First, understand just enough of the project shape to avoid generic advice:

- Main application entry points
- Domain/module boundaries
- Test setup
- CI/build commands
- Shared libraries/utilities
- Existing conventions
- Recently changed or high-churn areas if git history is available

For broad scans, load `CHECKLIST.md` before inspecting files. For targeted work, skip it and inspect only the relevant files and nearby tests.

Do not run destructive commands.

### 2. Identify hotspots

Look for maintainability problems in these categories, using `CHECKLIST.md` for the detailed scan prompts when needed:

- **Complexity:** code that requires too much local reasoning to change safely.
- **Duplication:** repeated business rules, orchestration, mapping, validation, config, or test setup.
- **Large files:** files with multiple responsibilities, not merely many lines.
- **Weak tests:** risky code with no behavioural guardrail, or tests coupled to private implementation.
- **Type/contract weakness:** module seams that rely on untyped data, nullable assumptions, or stringly states.
- **Weak interfaces:** callers must know ordering, invariants, intermediate state, or implementation details.
- **Operational/security maintainability:** repeated clients, env parsing, retry/idempotency, logging, or handler orchestration.

Do not suggest a candidate just because a category appears. Tie every candidate to a concrete future-change cost.

## 3. Present candidates

Present a numbered list of refactor candidates.

For each candidate, include:

- **Name** — short name for the candidate
- **Files** — files/modules involved
- **Category** — complexity, duplication, large file, tests, types, weak interface, operational/security
- **Problem** — what makes this hard to maintain
- **Evidence** — concrete examples from the code
- **Suggested change** — what should change
- **Why now** — why this is worth doing
- **Risk** — low/medium/high
- **Guardrails** — tests/checks needed before changing it
- **Estimated scope** — small/medium/large
- **Suggested first step** — the smallest safe next move

Use this format:

```markdown
## Maintainability Candidates

### 1. Extract shared request validation helper

- **Files:** `src/routes/create-order.ts`, `src/routes/update-order.ts`
- **Category:** Duplication
- **Problem:** Both routes implement similar validation and error mapping.
- **Evidence:** Same required field checks, same `400` response shape, same logging branch.
- **Suggested change:** Extract a shared validation function that returns a typed result.
- **Why now:** Reduces drift between create/update behaviour.
- **Risk:** Low
- **Guardrails:** Add route-level tests for current valid/invalid request behaviour.
- **Estimated scope:** Small
- **Suggested first step:** Add characterization tests before extraction.
```

Do not implement yet unless the user asked for changes.

Ask:

```text
Which candidate should I explore or implement first?
```

## 4. Prioritise recommendations

Prioritise candidates using this order:

1. High duplication of business rules
2. Large files with multiple responsibilities
3. Complex code with weak tests
4. Repeated infrastructure/config/error-handling code
5. Type weaknesses at module seams
6. Test duplication or noisy test setup
7. Cosmetic/readability-only changes

Prefer changes that reduce future bug risk.

Avoid spending time on purely stylistic changes unless they remove real confusion.

## 5. Implementation mode

When the user picks a candidate, follow this sequence.

### Step 1: Restate the target

Summarise:

- What will change
- What will not change
- Behaviour that must be preserved
- Files likely to be touched
- Tests/checks to run

### Step 2: Add guardrails first

Before refactoring, add or identify tests.

If tests are missing, add characterization tests around existing behaviour.

Do not change behaviour while adding guardrails.

### Step 3: Refactor incrementally

Make the smallest useful change.

Common patterns:

- Extract function
- Extract module
- Extract constants
- Introduce typed config/env parser
- Introduce test fixture builder
- Move helpers closer to their owning concept
- Split large file by responsibility
- Remove dead branches after tests pass
- Replace boolean flags with clearer functions/options

### Step 4: Verify

Run the project’s normal checks.

At minimum, run whichever are available:

```bash
npm test
npm run lint
npm run typecheck
npm run build
pnpm test
pytest
ruff check .
mypy .
```

If checks cannot run, explain why and provide manual verification steps.

### Step 5: Report back

After changes, summarise:

- What changed
- Why it is safer/easier to maintain
- Tests/checks run
- Any remaining risks
- Follow-up candidates

## What not to do

Do not:

- Rewrite large areas without approval
- Introduce new dependencies without a strong reason
- Extract abstractions just because code looks similar
- Move code across domain/module seams without understanding ownership
- Change public behaviour silently
- Change formatting-only across many files
- Create generic helpers with unclear names
- Hide important business rules behind vague utilities
- Ignore existing ADRs or project conventions
- Touch generated files, lockfiles, migrations, or snapshots unless necessary

## Output style

Be direct and specific.

Prefer:

```text
This file is doing three jobs: parsing input, applying business rules, and shaping the HTTP response. Split the business rule into a small module and keep the handler thin.
```

Avoid:

```text
The architecture could be improved by separating concerns according to clean architecture principles.
```

The user wants practical refactoring opportunities, not textbook architecture advice.
