---
name: design-plan-review
description: Use when a user wants independent Architect and Senior Engineer reviews of a proposed software design and implementation plan before implementation, including gaps, incorrect assumptions, feasibility and unnecessary complexity. For reviewing delivered code, use an implementation review instead.
metadata:
  author: "chearmstrong"
  canonical-source: "https://github.com/chearmstrong/skills"
---

# Design and Plan Review

Produce one evidence-based review through two fresh, independent reviewers.
Assess whether the design is appropriate and the plan can deliver it, rather than
checking document completeness alone. This skill owns delegation and consolidation;
it does not require any other installed skill.

## 1. Establish the shared brief

Read [the reviewer contract](references/reviewer-contract.md) before dispatch.
Resolve the design and implementation plan from the user's paths, attachments or
current task. State the chosen scope. If a requested document cannot be located,
identify the missing input before claiming a complete review. Review supplied
material without inventing the missing document or its decisions.

Capture the same design, plan and material linked decisions for both reviewers.
For repository files, record paths, base/head revisions where relevant, and
content digests. Freeze relevant uncommitted or untracked document contents in a
temporary directory outside the repository; digests alone are not a readable
snapshot. Preserve file paths and line numbers and record the in-scope inventory,
including staged/unstaged distinctions. For remote documents, capture the version
or retrieval date and content digest. Exclude secrets and disclose resulting gaps.

Build a factual brief containing:

- Intended outcome, constraints and acceptance criteria from the user and sources.
- Approved decisions, recommendations awaiting approval and implementation assumptions.
- Repository/worktree locations, document snapshot and connected source references.
- Existing capabilities, dependencies, operational constraints and verification evidence.
- Known missing sources and any expected load actually established by evidence.

Inspect connected code/configuration only where it could change the recommendation.
For stacked work, distinguish the existing base capability from what each proposed
change adds; verify ancestry when it matters. User count does not establish concurrency.
Do not seed the brief with the author's verdict or suggested findings.

## 2. Resolve guidance and capabilities

Core review criteria are bundled in this skill. Other skills are optional sources
of relevant criteria, never prerequisites. If selected, read them once, capture
entrypoints and needed references with paths/revisions or digests, and give both
reviewers the same guidance snapshot. Supporting skills' extra delegation,
implementation steps and separate report formats do not apply.

Use available repository evidence and primary external sources for consequential
platform claims. Check compatibility with pinned versions. Record unavailable
access or uncertain behaviour instead of treating a generic recommendation as a
project requirement. Browsing and specialised connectors are optional capabilities;
missing tools limit the evidence rather than justify an invented answer.

Confirm that the host both supports and permits delegation. If it does not,
report that independent review cannot run and stop before dispatch. Do not invoke
another delegation skill or label a self-review as two independent reviews.

## 3. Dispatch exactly two reviewers

Use the host's native agent tools directly. Start exactly two fresh reviewers
with clean contexts, default model and reasoning effort unless explicitly
overridden. In Codex use `fork_turns: "none"`; use the equivalent isolation on
other hosts. Run them in parallel when supported; otherwise run the two clean
contexts sequentially with the same neutral brief and no shared conclusions.

Give each the shared brief, complete readable snapshot, bundled reviewer contract,
selected guidance, role, expected verification and explicit read-only scope.
Both review the entire design and plan together; do not divide the documents.

- **Architect:** emphasise ownership, interfaces, dependency direction, data and
  trust boundaries, assumptions, operational responsibilities and simpler alternatives.
- **Senior Engineer:** emphasise implementation feasibility, failure paths,
  security, concurrency, recovery, performance, compatibility and meaningful tests.

Both check design/plan consistency and simplicity. Reviewers may inspect connected
source and suitable primary references within scope, but cannot edit files, run
implementation work, publish feedback or delegate further. Existing test results
are evidence only for the revision and behaviour exercised. Run additional safe,
focused checks only to resolve a named consequential uncertainty; temporary
outputs stay outside the reviewed repository.

If a reviewer fails, report incomplete independent coverage. Clarification may use
the same reviewers; do not silently replace one or expand the reviewer count.

## 4. Validate and consolidate

Read [the report format](references/report-format.md) after the reviews return.
Validate candidate findings against the snapshot, connected source, requirements
and any external evidence. Deduplicate by underlying cause. Agreement is not
proof; retain an evidenced finding even if only one reviewer raised it. Explain
material unresolved disagreement rather than averaging severity.

Check coverage of the intended outcome, material decisions and verification in
the plan. Classify each accepted item as a required refinement, a decision needing
owner input, or an optional improvement, using the reviewer contract. Prior
approval does not prevent a supported challenge to a design; a challenge remains
a proposal until authorised.

Before reporting, compare the document inventory, staged/unstaged state and
content digests with the snapshot. Account for additions, deletions and renames,
not just edits to the original files. Record connected source revisions inspected.
If inputs drift, tie findings to the reviewed snapshot and qualify coverage of
later content. A missing source or unconfirmed suspicion belongs in limitations,
not a confirmed defect.

Return one consolidated report. No findings is valid. Readiness is an assessment,
not permission to implement or approval of unresolved policy decisions. Leave
source files, plans, Git state and external systems unchanged.

Example: `$design-plan-review path/to/design.md path/to/implementation-plan.md`

## Authoring checks

When changing this skill, use [the scenarios](references/scenarios.md). Record
independent behavioural tests separately from structural checks and manual walkthroughs.
