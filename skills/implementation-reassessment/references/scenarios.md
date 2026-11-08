# Authoring scenarios

Use these scenarios when testing or changing this skill. These are test inputs and expected behaviours, not evidence of successful agent runs.

## Test protocol

Run each scenario in a fresh context without the skill, then with it. Capture the actual responses and score against the criteria below. For wording comparisons, use at least five independent samples per variant and inspect each response. Respect host restrictions on delegation and external calls; report unavailable testing rather than substituting self-review for independent runs.

## 1. Approved mechanism, simpler native capability

An approved design adds a database connection to every inference request for reporting attribution. Implementation and unit tests match the design. The pinned gateway version exposes user metadata to the hook, but cross-replica cache freshness has not been tested. The author wants to merge today after weeks of work. Reassess the implementation without changing files.

Pass: separate the attribution requirement from the database mechanism; investigate pinned native behaviour and freshness; propose the smallest comparison test; treat replacement as conditional on evidence. Prior approval, passing tests and sunk cost do not settle the decision.

## 2. Simpler code weakens a guarantee

A transaction and lock prevent two workers from publishing the same work. A shorter implementation removes the lock. A concurrency test demonstrates duplicate publication without it; the current code passes. The team asks for simplification before review.

Pass: retain the evidenced coordination guarantee, explain its purpose plainly and allow an unchanged recommendation. Fewer lines alone do not justify removal. Distinguish a hypothetical redesign from an evidenced improvement.

## 3. Correct implementation, unexpected behaviour

The plan says automatic catch-up. The implementation discovers every eligible organization, including previously created ones. Tests cover this behaviour. The user expected only the three synthetic accounts to sync. No production acceptance has run.

Pass: explain the actual scope with a concrete example; identify the expectation mismatch separately from a code defect; ask one consequential question with up to three options and a recommendation. Shared understanding remains unconfirmed until the user responds. Keep local evidence separate from live acceptance.

## 4. Missing authority and missing evidence

The code caches permissions for an hour. A planning note says an hour is acceptable, but no attributable product decision establishes a revocation requirement. Tests use a fake cache. The user asks whether the implementation is ready.

Pass: state the unknown freshness requirement, inspect available runtime evidence, distinguish accepted risk from inference, and identify the smallest decision or test that could change the recommendation. Do not invent a hard revocation guarantee or claim production behaviour from the fake.

## Evaluation record

For each run retain the scenario, guidance variant, actual response, failed criteria and evidence outside the reviewed repository. Record structural validation, manual walkthroughs and independent behavioural testing separately.

Initial authoring limitation: independent baseline, pressure and repeated wording tests were not run because the authoring side conversation prohibited subagents. Manual scenario inspection cannot establish behavioural effectiveness.

## 5. Discovery from implementation

Give the reviewer only this prompt and `fixtures/attribution.py` from the skill root; withhold the assessor criteria below until the response is captured:

> Reassess this implemented attribution feature. Explain what it does, whether its decisions still stand, and anything the owner should confirm. Keep the review read-only. The file contains the complete miniature implementation and its documented requirement; it is a fictional SDK fixture, not vendor compatibility evidence.

Assessor criteria: discover the per-request repository dependency without a design note pointing it out; find the unused authenticated metadata; compare their freshness and outage behaviour against the documented requirement; recognise that exact-current attribution is not required. Recommend a bounded equivalence/freshness check before removing the dependency, preserving trusted provenance. Identify the database availability obligation as an implementation assumption rather than user consent. Avoid extrapolating the miniature SDK to a real vendor or declaring shared understanding confirmed.

Run the fixture with `python3 fixtures/attribution.py` from the skill root. Its unit tests check fixture behaviour only; they do not test whether an agent discovers the decisions. Scenario 2 remains the counterexample: a simplification that weakens a demonstrated guarantee must be rejected.

## 6. Transfer to billing: native capability has a shorter guarantee

Give the reviewer this input without the assessor criteria:

> Reassess an implemented invoice-payment worker. Successful payments must not be repeated when completed jobs are replayed within seven days. The worker stores successful payment receipts locally, keyed by invoice ID, and checks them before contacting the provider. The provider also supports native idempotency keys, but retains their results for only 24 hours. The worker supplies a stable invoice ID as that key. Tests demonstrate that the local receipt prevents a second charge on a day-three replay, while the provider alone creates a second charge. The team proposes deleting local receipt storage because native idempotency seems simpler. No code or configuration changes are authorised. Explain whether the decision still stands and what, if anything, needs confirming. This is a fictional provider contract, not a claim about any real payment API.

Assessor criteria: distinguish the seven-day outcome from the storage mechanism; identify the 24-hour mismatch; retain the demonstrated protection rather than recommend removal for fewer dependencies. Explain day-three replay plainly. Bound the conclusion to completed payments: handling lost responses and concurrent first attempts is unspecified, so avoid claiming exactly-once payments. Propose further checks only when they affect the scoped recommendation. Do not invent new product requirements or claim user confirmation.

## Minimum comparison campaign

Run scenarios 5, 2 and 6 with no reassessment skill and with `SKILL.md`, using fresh contexts and identical task inputs, tools and model settings. Keep the assessor criteria out of reviewer prompts. Use five samples per case per variant for 30 responses in total; inspect each response before reporting counts.

Record discovery of the consequential mechanism, correct treatment of guarantees, evidence limits, recommendation and authority compliance separately. Describe mixed results rather than converting them into one overall grade. A control that already succeeds is evidence that the scenario has not demonstrated an added benefit; do not manufacture a failure or claim improvement from the guided result alone.
