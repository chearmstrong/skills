# Validation And Reporting

## Evidence Standard

A reportable bug needs one or more:

- Reproduction steps or failing command.
- Failing or absent regression test tied to a specific invariant.
- Static trace from attacker/user/input/source to sink.
- Contradiction with documented behaviour, schema, migration, or API contract.
- Comparison with a working local pattern that proves this path is inconsistent.

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
- **Low**: real but narrow bug, dead branch hiding intended behaviour, misleading error handling, or missing test for a fragile invariant.

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
