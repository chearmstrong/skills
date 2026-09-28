---
name: architecture-compliance-check
description: Verify architecture, implementation, and documentation against documented patterns, project rules, and authoritative evidence. Use when reviewing code, reconciling documentation or canonical-source drift, assessing reusable assets or platform alternatives (including OSS/Enterprise, version, and client capability differences), deciding whether a proposal is ready for agreement, reviewing architecture spikes or delegated-workflow boundaries, or before architecture-affecting commits.
metadata:
  author: "chearmstrong"
  canonical-source: "https://github.com/chearmstrong/skills"
---

# Architecture Compliance Check

## Overview

Check whether a change still belongs to the architecture the repository has actually documented and implemented.

**Core principle:** architecture compliance is not "does this look sensible?" It is "can I point to the document, existing implementation, or user rule that permits this shape?"

## Select And Load The Review Mode

Choose one primary mode. Before applying it, read the required references below in full. Load another mode only when its question remains material after the first pass; do not load every reference for a narrow compliance review.

| Question | Mode | Required reading |
| --- | --- | --- |
| Does a proposed or implemented change fit the documented architecture? | **Compliance** | The compliance decision tree below and the affected boundary contract; no mode reference. |
| Is a consequential proposal ready for agreement? | **Decision-readiness** | [Decision Readiness](references/decision-readiness.md). |
| Does documentation match implementation and canonical sources? | **Documentation-evidence** | [Documentation Evidence](references/documentation-evidence.md). |
| Does a design spike mix current discovery with a future direction? | **Platform-spike** | [Platform Review](references/platform-review.md). |
| Should operational/delivery assets or platform alternatives be reused? | **Research and inventory** | [Platform Review](references/platform-review.md), including its inventory and decision gates. |
| Does a proposal add a first delegated workflow through shared infrastructure? | **Delegated-workflow design slice** | [Delegated Workflow](references/delegated-workflow.md) and [Platform Review](references/platform-review.md) for shared evidence, assumptions and coherence rules. |

When a platform-spike or research-and-inventory review compares vendor editions, versions, clients or supported integrations, read [Platform Capability Evidence](references/platform-capability-evidence.md) before assigning decision gates. Use its capability matrix and pilot proof alongside the existing evidence records. Do not load it for unrelated compliance reviews.

## Compliance Decision Tree

Use the smallest branch that answers the architectural question.

| Situation | Required evidence | Action |
| --- | --- | --- |
| Change follows an existing pattern | Existing implementation plus matching docs or tests | Reuse the pattern; cite the concrete file or doc section in the review/summary. |
| Change introduces a new pattern | ADR, design doc, issue/spec, or explicit user instruction | Stop if none exists. Add documentation or ask before implementing. |
| Change crosses a module or service boundary | Boundary contract, public interface, schema, event shape, or dependency direction | Verify both sides. Do not infer compatibility from one caller. |
| Change touches DynamoDB, retries, queues, or idempotency | User guardrails plus implementation tests | Treat missing pagination/idempotency tests as a compliance gap, not just a test gap. |
| Change touches CDK/IaC | Existing stack organisation, logical IDs, `cdk diff` expectations, security rules | Flag replacement, IAM, encryption, retention, and alarm changes explicitly. |
| Change relies on external API behaviour | Versioned dependency files plus official docs, Context7, AWS docs, or stable vendor docs | Prefer pinned-version evidence over generic latest examples. |
| Docs and code disagree | Running code, tests, config, and deployment artefacts | Do not choose the convenient source. State the conflict and fix docs or code deliberately. |

## Failure Modes To Hunt

These are the compliance bugs that often look like harmless cleanup:

- **Pattern laundering:** copying a nearby shape without checking whether it belongs to the same layer, tenant boundary, consistency model, or lifecycle.
- **Hidden contract changes:** altering return shapes, event schemas, pagination tokens, IAM resources, config names, or environment variables while treating the edit as internal.
- **Documentation drift:** updating implementation without updating the architecture doc, README, ADR, runbook, or example that future agents will treat as source of truth.
- **Boundary leaks:** making handlers know orchestration order, making domain modules know infrastructure details, or moving validation into a layer that cannot own the invariant.
- **Cloud footguns:** replacing stateful resources, broadening IAM, dropping encryption/retention, introducing hot-path scans, or assuming Lambda/SQS executes exactly once.
- **Best-practice cargo culting:** applying a framework recommendation that conflicts with the repository's pinned version, deployment model, or documented convention.

## Domain Traps

Check these traps before approving or finishing work:

- **DynamoDB:** preserve `LastEvaluatedKey` exactly; keep PK/SK immutable; treat GSIs as projections; use `Query` rather than `Scan` in hot paths; make retryable writes idempotent.
- **CDK/IaC:** preserve construct IDs; call out replacements; keep least-privilege IAM; retain stateful data; document `cdk diff` output before deploy/PR when infrastructure changed.
- **Portable skills:** keep `SKILL.md` as the source of truth; use only required frontmatter unless optional spec fields add value; keep product-specific files optional.
- **Documentation:** follow user, project, or publication language conventions; default to British English only when no stronger style is present; preserve quoted API/log spelling; keep docs aligned with implementation rather than aspirational architecture.

## Evidence Rules

- Prefer repository docs and existing code over generic advice.
- Prefer official or versioned external docs over blogs and examples.
- When using MCP tools, treat them as accelerators, not authority by themselves.
- If evidence is missing, report "not documented" as the finding; do not fill the gap with assumption.
- If a primary external source is unavailable, inaccessible, unversioned, or ambiguous, record the affected claim or gate as `unknown` and the reason. Secondary material may guide further investigation, but cannot turn that gate into `pass`.
- If the user explicitly authorises a new pattern, document the decision in the smallest appropriate place.

## Output Shape

When reporting compliance, include:

- **Evidence:** files, docs, tests, or official sources checked.
- **Verdict:** compliant, partially compliant, non-compliant, or undocumented.
- **Risk:** what could break if the mismatch remains.
- **Fix:** the smallest documentation, test, or implementation change needed.

## Anti-Patterns

Never:

- Approve a new architectural pattern because it resembles a familiar pattern from another project.
- Treat "there is similar code" as sufficient evidence without checking ownership and context.
- Move code across layers just to reduce duplication.
- Rewrite docs to justify accidental implementation drift.
- Hide a behavioural change behind terms such as cleanup, simplification, or refactor.
- Accept infra changes without checking replacement/IAM/security implications.
- Continue through an undocumented architectural decision when the user has not authorised it.
