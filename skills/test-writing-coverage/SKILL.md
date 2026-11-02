---
name: test-writing-coverage
description: Use when writing or reviewing automated tests, adding regression coverage, simplifying duplicated test setup or fixtures, investigating flaky tests, assessing redundant or low-value tests, or checking testing best practice across unit, integration, contract and end-to-end suites.
metadata:
  author: "chearmstrong"
  canonical-source: "https://github.com/chearmstrong/skills"
---

# Test Writing and Coverage

Judge a test by the realistic regression it catches and the cost of maintaining it. Use the same standard when proposing a test, reviewing it or deciding to remove it.

## Establish the context

- Follow the requested mode: review means findings without edits; writing or cleanup authorises in-scope test changes.
- Inspect repository instructions, the implementation and contract, neighbouring tests, shared setup, test configuration and CI commands. Discover the language, framework version, runner, package manager, working directory and selection rules from those sources. Do not impose a directory layout, async marker, fixture framework or evaluation harness.
- Identify the behaviour at risk and choose the lowest test level that can expose its failure. A mocked unit test cannot establish real database, protocol or cross-component compatibility; use a focused integration or contract test for that boundary.
- Check current official framework documentation when version-sensitive behaviour is uncertain. If documentation tools are unavailable, use official web documentation; report unresolved uncertainty rather than inventing a requirement.

## Shared quality decisions

For each test or related group, identify the promised behaviour, the realistic defect that should fail it, and whether the assertion observes that defect. Apply these decisions in both modes:

| Concern | Decision rule |
| --- | --- |
| Duplicated setup | Extract a fixture, factory or helper when the same preparation has the same meaning and changes together. Return fresh state and preserve visible scenario inputs. A few repeated lines can be clearer than indirection. |
| Parameterisation | Combine cases that exercise the same rule and assertion shape; give cases useful failure names. Keep different behaviours separate. Avoid conditional assertions, a combinatorial explosion or one helper with many switches. |
| Shared resources | Share expensive infrastructure only with explicit isolation and teardown. Sharing setup code is different from sharing mutable state; account for parallel workers, resource names and transaction boundaries. |
| Low-value tests | Investigate tautologies, expectations computed by production logic, mock-only checks, incidental snapshots, and tests that only restate source text or framework mechanics. Establish what they protect before classifying them. |
| Assertion strength | Assert the outcome and relevant side effects independently of the implementation. Call arguments, counts and order are valid when they are the contract: for example, exactly one payment for duplicate submissions. |
| Contract versus detail | Exact protocol bytes, published error text and compatibility values can be contractual. Private helper order, incidental copy and internal structure usually are not. Establish the promise before tightening or relaxing assertions. |
| Test doubles | Control external boundaries and failure conditions without replacing the behaviour under test. Match the dependency's relevant contract; use integration checks when a double could hide incompatibility. Mock count alone is not a defect. |
| Coverage | Use uncovered code to find plausible missed failures. Prioritise meaningful boundaries, error paths and regression history; neither line coverage nor case count establishes test value. Trivial forwarding needs a test only when it owns behaviour worth protecting. |
| Reliability | Check time, randomness, ordering, shared state, resource cleanup and unawaited work. A suspicious pattern is evidence of a risk, not proof of an intermittent failure. |

If a task includes intermittent failures, timing issues or a reliability finding, read [Flaky test investigation](references/flaky-tests.md) before classifying or fixing it. Skip that reference for other tasks.

## Review tests

1. Trace the test's setup and assertions through the relevant production path. Read nearby coverage and the original bug or requirement where available. Distinguish the test's claimed protection from what it actually exercises.
2. Classify a concrete recommendation as **keep**, **simplify**, **strengthen**, **remove** or **add**. A repeated shape is not enough to justify consolidation; distinct boundaries or regressions can deserve similar tests.
3. Before recommending removal, list the unique scenarios, assertions and failure modes it protects. Identify retained coverage for each, or explain why the behaviour is obsolete or the test protects no meaningful promise. If intent or replacement coverage is unclear, retain it and state the gap.
4. Rank findings by lost protection, misleading green results or unreliable execution before cosmetic simplification. Give a representative file/line, evidence, impact and smallest useful change. Group one repeated mechanism into one finding; avoid generic best-practice checklists as findings.

A review may conclude that the tests are already good enough. Do not manufacture changes to fill each category.

## Write or improve tests

1. Name the failure the test should catch before writing its body. Choose cases from the contract, changed behaviour and risk; inspect existing coverage before adding another case. If no meaningful failure can be named, reconsider whether a test is needed.
2. Derive expectations from hand-checked values, a trusted independent oracle or contract invariants. Exercise the real decision path and keep failure messages tied to the scenario.
3. Reuse existing setup where suitable; apply the shared quality decisions before introducing another abstraction.
4. For a bug regression, show the test fails on the broken behaviour and passes with the authorised fix. Confirm the failure is caused by the intended behavioural defect, rather than collection, import or setup errors. For a new behaviour, demonstrate the intended failure before implementation where feasible. If sensitivity is unclear, use an authorised disposable copy or existing broken revision; do not inject defects into the reviewed checkout. Record any limitation instead of claiming unobserved failure evidence.
5. If a corrected test exposes a production defect outside the authorised scope, preserve the reproducer and report it. Change an expectation only when the requirement changed or evidence shows the old expectation was wrong.

### Independent expectation example

Suppose the contract applies a 10% discount to 105 integer cents and rounds a half-cent upwards: 94.5 becomes 95. These illustrative Python test bodies use placeholder API names; the principle applies to any framework.

```python
# Weak: discounted_total uses the same production rounding helper.
expected = round_cents(105 * 0.9)
assert discounted_total(105, 10) == expected

# Independent: the expected boundary result comes from the contract.
assert discounted_total(105, 10) == 95
```

If the shared helper incorrectly rounds halves to even, both sides of the weak assertion become 94 and it passes. The independent assertion catches that defect.

## Verify and report

Discover the actual command and selection first: a green run that skips the relevant tests proves nothing about them. Choose verification by the reach of the change:

| Change or task | Verification scope |
| --- | --- |
| Read-only review | Trace the claimed protection in source; run focused tests when execution can resolve a material uncertainty. Distinguish static findings from observed outcomes. |
| Isolated test or assertion | Run the changed cases and demonstrate sensitivity to the intended failure. Include neighbouring cases when they share affected state or setup. |
| Shared fixture, factory or test helper | Run its consumers; include relevant order or parallel execution when isolation could change. If consumers cannot be identified reliably, widen to the affected suite. |
| Runner, discovery, markers or CI selection | Check collection and selection for affected targets, then run them through the changed entry point. A direct invocation cannot validate a broken default command. |
| Production behaviour or integration boundary | Run focused regressions plus affected component or integration suites; use the real boundary when that is the claim being verified. |

Combine applicable rows. Repository-required checks remain required; report unavailable checks and missing prerequisites rather than silently substituting narrower evidence. Respect the task's authority and environment constraints when choosing commands.

For removals or consolidation, check that the remaining cases are collected and still exercise the protected behaviours. Where overlapping tests run at different levels or CI stages, preserve the distinct integration evidence or earlier feedback they provide.

Scale the report to the risk: a small isolated change can use a few sentences; shared setup, runner changes or uncertain failures need enough detail to assess the wider impact. In either case, include:

- The review verdict or changes made, with the important behaviour protected and any remaining gap.
- Concrete findings or removals with their evidence and retained protection; separate confirmed defects from suspected risks.
- Commands, working directory and results, distinguishing passed, failed, skipped and not run. Include relevant failures even when pre-existing; if execution is unavailable, name the missing prerequisite and limit the conclusion.

## Never trade confidence for a green result

- Never weaken assertions, update snapshots blindly or delete a failing case just to pass: establish the intended behaviour and preserve the failure evidence.
- Never declare a test pointless solely because it is small, old, repetitive or already passes: show what protection is absent or retained elsewhere.
- Never impose coverage percentages, mock limits or a test per helper as universal quality rules: use project requirements and behavioural risk.
