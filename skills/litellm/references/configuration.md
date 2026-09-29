# Configuration and integrations

Read the task-relevant source links here and confirm behaviour in the selected
release. Avoid importing upstream example defaults as company policy.

## Configuration and routing

`model_name` is the client alias; `litellm_params.model` selects the provider route.
Make supported capabilities and regions explicit. Multiple deployments under
one alias can load balance; prove all destinations are approved. Treat model
fallback as a policy choice, not merely an availability knob.

Identify whether YAML or database-managed settings own each value. Database
overlays can make a YAML edit ineffective, while database models can add
deployments alongside YAML models. Check the resolved model list and settings
before diagnosing a reload issue. Do not enable database management by default
in a Git-owned configuration workflow.

Sources: [config and precedence](https://docs.litellm.ai/docs/proxy/configs),
[routing](https://docs.litellm.ai/docs/routing),
[retries and fallbacks](https://docs.litellm.ai/docs/proxy/reliability).

Bound attempts across the client, LiteLLM and provider SDK. Check the total
deadline and retry amplification under throttling. Do not silently drop
unsupported request parameters to make a request succeed; verify the client's
required semantics, model capabilities, and adapter support.

## Authentication and spend controls

Separate client authentication, user/team mapping, model permission, provider
authentication, and administration. A virtual key is a gateway credential; it is
not an upstream provider key. Native JWT inference authentication, UI SSO and
custom auth are separate integrations with edition-specific constraints.

For OSS custom auth, inspect the supported hook and returned identity contract.
Prove native model/budget enforcement still runs for that identity; returning a
validated user alone is insufficient. Never grant an administrative identity
just to bypass a rejected request. Keep management routes privately accessible
through the project's chosen access path.

Sources: [virtual keys](https://docs.litellm.ai/docs/proxy/virtual_keys),
[custom auth](https://docs.litellm.ai/docs/proxy/custom_auth),
[JWT auth](https://docs.litellm.ai/docs/proxy/token_auth),
[edition boundaries](https://docs.litellm.ai/docs/enterprise).

Link each inference key to the intended user/team. Distinguish team-member,
team, key and personal-user budgets; do not assume all limits accumulate.
Test with the intended restricted role, not the master key. Record accounting
delay and observed overshoot with concurrent/streaming requests. Test revocation,
team changes and database/Redis failures. Decide when requests must stop if
limits cannot be verified; a spend report alone is not budget enforcement.
Source: [budgets and rate limits](https://docs.litellm.ai/docs/proxy/users).

## Bedrock and client integration

Use the documented adapter/model string and credential chain for the selected
Bedrock API. On ECS prefer task-role credentials; locally validate credentials
inside the process/container making the call. Confirm region, model access,
inference-profile resources and any cross-region destinations. Do not assume a
provider prefix implies a particular AWS operation or data location.
Source: [Bedrock adapter](https://docs.litellm.ai/docs/providers/bedrock).

For an OpenAI-compatible client, configure its gateway base URL and a restricted
key. With a `/v1` base, avoid accidentally producing `/v1/v1`. Match Chat
Completions, Responses, or Anthropic-compatible requests to the client's actual
surface. Exercise streaming and tool calls with that client before declaring
compatibility. For in-process calls and routing, load
[Python SDK patterns](python-sdk.md).
Source: [proxy quickstart](https://docs.litellm.ai/docs/proxy/quick_start).

## Telemetry and extensions

Use the supported OpenTelemetry callback/exporter for the chosen release.
Confirm endpoint, protocol, dependency extras and resource attributes with the
collector configuration. An endpoint environment variable alone does not prove
instrumentation is enabled. Do not assume another application's telemetry
wrapper applies automatically to the LiteLLM process.

For a task-local collector, check callback activation (current docs use `otel`),
the sidecar listener's HTTP/gRPC protocol and task-local endpoint, exporter
dependencies, and content policy. Current docs use
`OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT=NO_CONTENT`; verify the pinned
release and each handler's override. Inspect an exported synthetic trace to prove
delivery and content exclusion rather than relying on configuration alone.

Inspect message capture, spend logs, callbacks, exception bodies and debug output.
Verify that metadata-only exports exclude prompts, responses, file contents,
credentials and authentication tokens while retaining token counts and spend.
Optional exporter failure and authoritative spend loss
need separate failure policies. Preserve request correlation without trusting
client-supplied user/team values as authorisation.
Source: [OpenTelemetry integration](https://docs.litellm.ai/docs/observability/opentelemetry_integration).

When extending LiteLLM with auth hooks, callbacks or middleware, verify the
public extension point and its sync/async contract in the pinned release.
Package it into the selected image and test import/startup before cloud rollout;
avoid patching internal/private functions as the first integration approach.
