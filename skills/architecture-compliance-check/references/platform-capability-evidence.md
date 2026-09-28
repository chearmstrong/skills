# Platform Capability Evidence

## Establish Whose Statement It Is

Record the source and author of each decision-changing statement. A customer agenda or requirement describes desired behaviour; vendor documentation describes advertised capability; a tagged implementation shows a particular code path; a pilot demonstrates behaviour only in its tested configuration. Keep those forms of evidence separate.

Use an ambiguous agenda phrase as a discovery question, not proof of a product feature. Ask whether the behaviour exists today, needs configuration, requires an integration or belongs to a roadmap.

## Compare The Exact Capability

Add one row per material requirement to the existing evidence matrix:

| Field | Required evidence |
| --- | --- |
| Requirement and owner | Desired outcome, who supplied it, decision/action it affects, and acceptance criterion. |
| Product and edition | OSS, paid edition or custom integration; feature/licence terms and support constraints for the intended use. |
| Version and execution surface | Release/tag, CLI/Desktop/server or other client, supported OS and deployment/configuration path. Mark untested combinations explicitly. |
| Implementation path | Built-in feature, configuration, supported extension, existing company component, proposed new component or roadmap claim. |
| Control boundary | Component that enforces the requirement, caller identity, override/bypass paths, and relevant policy/data dependencies. |
| Proof and gate | Official source or tagged code, checked date, runtime result, remaining unknown, owner and smallest pilot check; use the skill's existing gate states. |

Documented availability, static implementation and runtime validation are different claims. Do not label a configuration or edition as validated because a different edition, release, client or authentication path was evaluated internally.

Resolve documentation/source conflicts against the intended release. Code inspection cannot settle commercial entitlement, and a licence page cannot prove a runtime path. If either source is unavailable or ambiguous, keep the affected claim `unknown` and identify the next check.

## Test Enforcement Rather Than Defaults

Choose only checks that can change the recommendation. For each pilot, name the requirement, tested configuration, positive and negative case, pass criterion and evidence to retain.

| Requirement | Consequential pilot proof |
| --- | --- |
| Managed configuration | Show which source wins when user/project settings conflict, whether the policy can be bypassed, and how an installed extension actually loads on each intended client/OS. |
| Corporate identity | Trace login/token renewal to request validation and user/team mapping; check expiry, revocation and denied access. A static-key evaluation does not validate this path. |
| Mandatory gateway | Attempt alternative provider configuration and direct access; identify the client, network or server control that blocks bypass. A recommended endpoint alone is a default. |
| Budgets and model policy | Show per-user/team attribution, allowed and denied models, limit rejection and accounting through the selected auth/extension path. Inspect persistence/failure handling when durable spend control is required. |
| Version management | Test the update mechanism separately for each intended client; a shared configuration flag need not control every distribution's updater. |

One successful request proves that request path, not enforcement, recovery or all supported clients. Report untested surfaces rather than extrapolating from a laptop demo.

## Recommend Without Inventing Infrastructure

Compare supported built-in behaviour, configuration, extension points and reusable company components before proposing a new proxy, fork or service. A paid feature does not establish that it is the only supported route to the required outcome; an extension hook does not establish that it preserves policy or accounting.

Compare licence cost with the evidenced work to build, secure, operate and upgrade the equivalent integration. Keep gateway/runtime placement, infrastructure tooling and model hosting as separate choices. Do not inherit sizing, service splits or operating promises from another edition without checking their dependencies.

Return a preferred option or a bounded evaluation, its trade-off, named validation gates and a concrete re-entry condition for discounted alternatives. Reconcile the recommendation, comparison, decisions and diagram labels so a proposed path never appears validated elsewhere.
