# Python SDK patterns

Use this for in-process calls and routing. Examples are adaptable and have not
been run against a provider. Pin the package and check the selected release's
adapter behaviour before using them.

## Choose the integration

| Need | Pattern |
| --- | --- |
| One direct provider call | `completion` for synchronous code; `acompletion` for async code |
| In-process aliases, load balancing or approved fallbacks | Construct `Router` once in application startup; call `router.acompletion` in async paths |
| Shared HTTP access, virtual keys, teams and gateway spend controls | Run the proxy and use a compatible HTTP client |

An in-process Router does not provide the proxy's HTTP authentication or
virtual-key administration. Keep credentials, authorisation and resource
cleanup in the host application's lifecycle. Do not add a proxy for an SDK-only
task. Source: [Router](https://docs.litellm.ai/docs/routing).

This illustrative Bedrock pattern takes the approved provider route and region
from the application's configuration layer. `coding` is a client alias. It
requires Python 3.11+ for `asyncio.timeout`. The 20/30-second limits illustrate
per-call and overall bounds, not production defaults.

```python
import asyncio

from litellm import Router


def build_router(provider_model: str, aws_region: str) -> Router:
    return Router(
        model_list=[{
            "model_name": "coding",
            "litellm_params": {
                "model": provider_model,
                "aws_region_name": aws_region,
            },
        }],
        num_retries=0,
    )


async def smoke_check(router: Router):
    async with asyncio.timeout(30):
        return await router.acompletion(
            model="coding",
            messages=[{"role": "user", "content": "Reply with OK"}],
            timeout=20,
            drop_params=False,
        )
```

Build the Router at startup, then pass it to request handlers. Confirm timeout,
retry and cleanup behaviour in the pinned package. This example disables Router
retries. Current Router docs also describe disabling provider-client retries;
confirm that behaviour in the selected release and adapter.

## Preserve request semantics

- LiteLLM normally raises `UnsupportedParamsError` for unsupported OpenAI-style
  parameters. `drop_params=True` discards them; it is an explicit change to request
  semantics, not a harmless compatibility fix.
- Keep dropping disabled when tools, structured output or other parameters are
  required. Check adapter/model support and test the returned behaviour. A
  successful response alone does not prove a constraint was honoured.
- If optional parameters may be dropped, identify them at the call site and
  test that policy. Avoid a process-wide `litellm.drop_params=True` that changes
  unrelated calls.

Source: [Parameter handling](https://docs.litellm.ai/docs/completion/drop_params).

## Bound retries and streaming

- Choose the layer that owns retries. `num_retries` controls LiteLLM's retry
  loop; provider SDKs use their own settings, such as `max_retries`. Current
  Router docs say Router pins provider retries to zero. Verify the chosen
  release/adapter; inspect transport retries separately for direct SDK calls.
- Check retry precedence: per-request values can override deployment and Router
  defaults. Do not accept caller-controlled retries beyond the application's
  budget.
- Include application retries, Router/SDK retries, provider retries and fallback
  destinations in the call budget. For nested retry loops without fallbacks,
  the upper bound is the product of each layer's allowed attempts, not their sum.
- Set a total deadline as well as per-call timeouts. Test throttling and count
  upstream attempts. An expired local deadline does not prove the provider has
  cancelled processing or stopped charging.
- For streaming, await `acompletion(..., stream=True)` and consume it with
  `async for`. Handle exceptions during iteration as well as stream creation;
  close the stream using the selected release's supported cleanup method on
  completion, cancellation or error. Do not replay an entire response after
  emitting chunks without an explicit application policy.

Sources: [Router retry ownership](https://docs.litellm.ai/docs/routing),
[SDK retries](https://docs.litellm.ai/docs/completion/reliable_completions),
[Async and streaming](https://docs.litellm.ai/docs/completion/stream).

## Classify errors before retrying

LiteLLM maps provider failures to named exception classes, available from
`litellm`. Match specific subclasses before their parent classes:

| Exception | Meaning and next action |
| --- | --- |
| `UnsupportedParamsError`, `ContextWindowExceededError`, `ContentPolicyViolationError` | Specific `BadRequestError` cases; fix parameters/input or apply an approved fallback policy |
| `BadRequestError` | Invalid request; repeating it unchanged is unlikely to help |
| `AuthenticationError`, `PermissionDeniedError`, `NotFoundError` | Check credentials, access and model/route; do not retry blindly |
| `RateLimitError` | Throttling; bounded backoff within the total deadline |
| `Timeout`, `APIConnectionError` | Timeout/connection or unmapped failure; inspect evidence before retrying |
| `ServiceUnavailableError`, `InternalServerError`, `APIError` | Service failure; apply the chosen transient-error policy |

Check type, status and redacted provider context rather than matching message
text. `llm_provider` identifies the adapter; it alone does not prove a request
reached the provider. Do not log full exception bodies that may contain content
or credentials. Source: [Exception mapping](https://docs.litellm.ai/docs/exception_mapping).

## Calculate cost without claiming enforcement

For a completed non-streaming response, use
`completion_cost(completion_response=response)`. This calculates cost from usage
and LiteLLM's model pricing data; it does not enforce a budget or establish the
provider's invoice. Confirm the actual provider route, region and applicable
pricing, including cache or special token charges.

For streams, obtain final usage or build the completed response with the
documented `stream_chunk_builder`; do not charge each delta as a separate
completion. Treat interrupted streams, missing usage or unknown model pricing
as incomplete accounting, not zero cost. Reconcile estimates with provider
billing and, for a proxy, its spend records.
Sources: [Usage and cost](https://docs.litellm.ai/docs/completion/token_usage),
[Streaming response builder](https://docs.litellm.ai/docs/completion/stream).
