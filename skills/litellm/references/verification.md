# Troubleshooting and verification

Collect bounded, redacted evidence: image/version, config digest, route, request
ID, model alias, HTTP status, elapsed time, task exit reason and dependency state.
Start with the smallest failing synthetic request. Preserve the original error
before changing configuration. Error names are clues; verify whether the failure
occurred in the client, edge, proxy, credential chain or provider.

## Follow the failing boundary

| Symptom | First checks | Verification after a fix |
| --- | --- | --- |
| Container exits before listening | Architecture, entrypoint/flags, extension imports, config file, env references, writable paths, schema step | Start the exact image/config and inspect exit/startup evidence |
| Probe works, inference fails | Calling key's aliases/permissions, provider route, credential resolution, Bedrock model/profile/region | Restricted-key request reaches the intended provider |
| Config edit has no effect | Delivered artefact/digest, restart/reload behaviour, DB overlays | Inspect resolved settings and exercise the changed behaviour |
| Requests stop during streaming | Actual API/events, edge buffering, idle gaps, client/gateway timeout, task termination | Full stream, cancellation and rolling-deploy tests |
| Throttling persists | Provider quota, shared limits, cooldowns, retries at each layer | Bounded burst test and measured recovery |
| Spend missing or budgets bypassed | Key identity/role, user/team linkage, accounting buffer, dependency errors | Reconcile requests/spend; rejected requests at the applicable limit |
| Telemetry absent or includes content | Callback activation, protocol/endpoint, exporter deps, capture switches | Inspect exported synthetic traces and failure handling |

Use [health contracts](https://docs.litellm.ai/docs/proxy/health),
[exception mapping](https://docs.litellm.ai/docs/exception_mapping), and
[debugging guidance](https://docs.litellm.ai/docs/proxy/debugging).
Check the selected image has any executable used in an ECS container health
command; do not assume `curl` is installed. Avoid provider-calling health checks
as high-frequency liveness probes.

## Match the claim to its evidence

| Claim | Required evidence |
| --- | --- |
| Config/IaC is structurally valid | Relevant schema, build, assertions and synth checks |
| Process is alive | Proxy liveness probe on the actual container port |
| Configured dependencies are ready | Readiness plus explicit DB/Redis checks needed by this deployment |
| Inference works | Representative synthetic request, expected provider route and completed response |
| Coding client works | Client-specific streaming, continuation and tool round trip |
| Model access is enforced | Allowed request and denied model/key/identity cases |
| Budgets are enforced | Restricted identity reaches limit and subsequent requests are rejected; concurrency and failure cases tested |
| Spend is durable | Restart/outage recovery, reconciliation and duplicate/missing-record checks |
| Upgrade is safe for the tested scope | Migration, overlapping-version, streaming/draining and rollback rehearsal |

Current readiness can report success with no database configured; read the
payload and confirm required persistence exists. Neither readiness nor a
populated `/key/info` is an enforcement test. Never claim runtime verification
from documentation, mock tests or a successful CDK synth.

## Prove rate limits at the claimed scope

Record the exact image/version, edition, effective key/user/team/model limits,
Redis coordination settings, route and environment. Current LiteLLM
[rate-limit documentation](https://docs.litellm.ai/docs/proxy/users) describes
RPM, TPM and `max_parallel_requests` at several identity scopes and Redis
coordination across instances. Treat that as documented capability; check the
selected release and measure the deployed behaviour before claiming a shared
ceiling. Use a restricted virtual key with fresh counters, synthetic traffic
and known retries; the master key does not exercise an unset key limit.

| Claim | Minimum proof | Boundary |
| --- | --- | --- |
| Limit is configured | Inspect the effective settings for the exact key, user, team or model and the delivered image/configuration | Configuration alone does not prove rejection |
| Key RPM or TPM works locally | In the exact image, exceed one limit with a controlled burst; capture successes, a gateway `429` with `rate_limit_type` of `requests` or `tokens`, then recovery after reset | Proves only that key, route and local runtime; test RPM and TPM separately |
| User or team limit is shared | Use distinct keys linked to the same user or team and show their combined traffic reaches that identity's limit | One key reaching its own limit proves nothing about the shared scope |
| Concurrency is enforced | Hold the allowed number of requests in flight, then check the next request's rejection and subsequent recovery | Repeat through separate replicas before claiming a cluster-wide ceiling |
| Limit is shared across replicas | Send requests deliberately through each instance using the same restricted identity and Redis; observe the combined limit, reset and measured overshoot | Test the Redis-unavailable policy separately; one proxy's result is insufficient |
| Limit works in an environment | Repeat the relevant restricted-key test through that environment's public route and correlate edge and gateway evidence | Local proof does not establish dev or production behaviour |

Use the [error reference](https://docs.litellm.ai/docs/proxy/error_reference)
to distinguish a gateway limiter `429` from provider throttling. An edge `403`
or an authentication rejection occurs before a rate-limit check and cannot
prove whether the limiter works. For an explicitly zero-priced model, budget
checks can be skipped; verify its RPM/TPM or concurrency controls separately.
Zero recorded LiteLLM cost does not establish zero provider cost. Confirm the
zero-price and rate-limit behaviour in the selected release before relying on
it as an admission control.
