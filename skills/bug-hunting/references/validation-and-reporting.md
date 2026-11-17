# Validation And Reporting

## Evidence Standard

A reportable bug needs evidence of incorrect behaviour or a concrete violated invariant, supported by one or more:

- Reproduction steps or failing command.
- Failing regression test demonstrating incorrect behaviour or a violated invariant.
- Static trace from attacker/user/input/source to sink showing how a reachable path violates expected behaviour or an invariant.
- Contradiction with documented behaviour, schema, migration, or API contract.
- Comparison with a working local pattern that proves this path is inconsistent.

Missing coverage is a verification gap, not proof of a bug. Describe it under verification limits or residual risk, and recommend a focused test where it would resolve uncertainty. Only report a bug when evidence meets the standard above.

Do not report:

- Style-only issues.
- Pure speculation without a reachable path.
- Framework-default concerns without checking the framework behaviour.
- Generic "could be null" claims when the type/schema/runtime guard excludes null.
- Existing issues outside a diff unless the user requested a broader audit.

## Severity

- **Critical**: likely unauthorised access, data loss/corruption, secret exposure, remote code execution, or destructive infrastructure change.
- **High**: credible security bypass, cross-tenant leak, non-idempotent duplicate write, major outage path, or resource replacement risk.
- **Medium**: incorrect behaviour under realistic edge cases, partial failure, pagination loss, retry bug, missing guard with bounded blast radius.
- **Low**: real but narrow bug, dead branch hiding intended behaviour, or misleading error handling.

## Final Response Shape

Findings first:

```text
File:Line - Short title
Severity: High
Problem: What goes wrong.
Why this is real: Concrete evidence.
Fix or verification step: Minimal next action.
```

Then include:

- Reviewed scope.
- Verification performed.
- Areas not reviewed or not fully verifiable.
- Tests or commands that could not be run.

If there are no findings:

```text
No significant bugs found in the reviewed scope.
Reviewed: ...
Verification: ...
Residual risk: ...
```

Avoid "clean", "safe", or "no bugs exist" for broad or partially reviewed scopes.
