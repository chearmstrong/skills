# Flaky test investigation

Use this reference when reviewing a reliability risk, investigating intermittent failures or changing timing-sensitive tests. The aim is a causal explanation and reliable assertions, with evidence limits made explicit.

## Classify the evidence

| Evidence | What it supports |
| --- | --- |
| Sleep, unseeded randomness, shared state or an unawaited task found in code | Suspected reliability risk; identify the plausible failure mechanism. |
| One failing run | A failure requiring diagnosis; it may be a deterministic defect, environment problem or intermittent failure. |
| Pass and fail on different revisions or materially different environments | An unexplained difference; compare conditions before calling it a flake. |
| Pass and fail on the same revision under comparable intended conditions | Observed intermittent failure; this establishes the symptom, not its root cause. |
| Isolated runs pass but a recorded order or concurrent run fails | Evidence of an ordering or concurrency dependency; identify the interfering state or resource. |

## Collect and isolate

1. Capture the revision, exact command, selected case, failure trace, runner/version, environment, seed, order, worker count and retry behaviour where available. Check whether retries or expected-failure settings are hiding the first failure.
2. Use existing CI history first. Choose a bounded run count or time budget appropriate to test cost and failure frequency; record it. Run the case repeatedly in isolation, then with relevant neighbours, altered order or parallelism according to the suspected mechanism. Change one relevant condition at a time.
3. Compare failures, not just pass rates. Separate product races, test races and unavailable infrastructure; a real concurrency bug must not be relabelled as test noise.
4. If reproduction fails, retain the observed history and suspected mechanism. Report "not reproduced in N runs"; no finite green sample proves the flake is gone. If execution is unavailable, report static risk only and the next evidence needed.

## Choose a causal fix

| Mechanism | Appropriate response |
| --- | --- |
| Waiting an arbitrary duration | Await the operation or observable completion with a bounded timeout and useful diagnostics. A longer sleep changes probability, not synchronisation. |
| Behaviour intentionally depends on time | Use supported clock control and advance through the relevant boundary. Account for scheduler/microtask behaviour; a frozen clock alone may stall work. Keep real timing checks when timing itself is the integration contract. |
| Shared data or order dependence | Give cases isolated state, reset global patches/environment, and clean up even after failure. Check worker-specific names, ports and filesystem paths. Serialisation can diagnose a race but does not establish a fix. |
| Random data | Use a reproducible seed and record it; retain meaningful variation. Do not choose a seed merely because it avoids a product defect. |
| Network or service variation | Keep deterministic tests controlled at the boundary; retain separately identified integration coverage of the real dependency. Diagnose service readiness and environment failures explicitly. |
| Tasks outlive the test | Await or cancel and join them; release owned resources during teardown. A passing assertion before background failure is misleading. |

## Verify the change

Re-run the previously failing conditions and a comparable bounded sample, including affected neighbours or parallel execution. State both the causal evidence and the sample size. Verify the assertions still detect the promised failure; suppressing an error or waiting forever is not a reliability improvement.

Never add retries, skip markers, quarantine or inflated timeouts merely to obtain green CI: these can conceal failures and reduce protection. If temporary containment is explicitly authorised, keep the failure visible, define the owner and follow-up or exit condition, and report it as containment rather than a fix. Existing intentional retries are evidence to inspect, not a reason to remove policy unasked.
