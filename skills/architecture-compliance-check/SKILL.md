---
name: architecture-compliance-check
description: Verify architecture and implementation follow documented best practices, project patterns, and user rules. Check against project documentation, ensure no assumptions are made, and verify implementation matches documented patterns. Use when reviewing code, implementing features, making architectural decisions, or before committing changes.
---

# Architecture Compliance Check

## Overview

Check whether a change still belongs to the architecture the repository has actually documented and implemented.

**Core principle:** architecture compliance is not "does this look sensible?" It is "can I point to the document, existing implementation, or user rule that permits this shape?"

## When to Use

**Mandatory checks:**
- Before committing architectural changes
- When implementing new features
- When reviewing code for merge
- When making design decisions
- When refactoring existing code

**Use especially when:**
- Implementing patterns from documentation
- Working with multi-component systems
- Making assumptions about behaviour
- Code doesn't match existing patterns

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

## Project-Specific Traps

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

## Integration with Other Skills

**Works with:**
- `systematic-debugging` - Verify root cause before fixing
- `verification-before-completion` - Verify compliance before claiming done
- `receiving-code-review` - Verify feedback against documentation
- `requesting-code-review` - Include compliance check in review

## The Bottom Line

Compliance means the change has traceable evidence. If the evidence is missing, the correct result is "undocumented", not "probably fine".
