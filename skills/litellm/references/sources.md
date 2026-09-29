# Primary sources and reference patterns

Source map checked on 29 September 2026. This date records documentation review,
not live deployment testing. Recheck release-sensitive behaviour against the
chosen version; current web docs and upstream `main` can be newer than it.
Prefer matching release source/tests when documentation differs. If live docs
are unavailable, state the assumption and leave the relevant behaviour unverified.

| Need | Primary source |
| --- | --- |
| First proxy/client path | [Quickstart](https://docs.litellm.ai/docs/proxy/quick_start) |
| Config shape, env references, YAML/DB precedence | [Configuration](https://docs.litellm.ai/docs/proxy/configs) |
| Runtime, data stores, migration and service layout | [Deployment](https://docs.litellm.ai/docs/proxy/deploy) |
| Pool sizing, workers, logging and production settings | [Production practices](https://docs.litellm.ai/docs/proxy/prod) |
| Models, credentials and Bedrock API selection | [Bedrock adapter](https://docs.litellm.ai/docs/providers/bedrock) |
| User/team/key limits | [Budgets](https://docs.litellm.ai/docs/proxy/users) |
| Virtual-key lifecycle | [Virtual keys](https://docs.litellm.ai/docs/proxy/virtual_keys) |
| Stored credentials, salt and master-key changes | [Key rotation](https://docs.litellm.ai/docs/proxy/master_key_rotations) |
| Retry/fallback behaviour | [Reliability](https://docs.litellm.ai/docs/proxy/reliability) |
| In-process routing and async calls | [Router](https://docs.litellm.ai/docs/routing), [Async/streaming](https://docs.litellm.ai/docs/completion/stream) |
| SDK parameters, retries and errors | [Parameter handling](https://docs.litellm.ai/docs/completion/drop_params), [SDK reliability](https://docs.litellm.ai/docs/completion/reliable_completions), [Exception mapping](https://docs.litellm.ai/docs/exception_mapping) |
| SDK usage and cost estimates | [Usage and cost](https://docs.litellm.ai/docs/completion/token_usage) |
| Liveness, readiness and provider probes | [Health](https://docs.litellm.ai/docs/proxy/health) |
| Callback/exporter and content capture | [OpenTelemetry](https://docs.litellm.ai/docs/observability/opentelemetry_integration) |
| Custom identity integration | [Custom auth](https://docs.litellm.ai/docs/proxy/custom_auth) |
| Native JWT integration and licensing | [JWT](https://docs.litellm.ai/docs/proxy/token_auth), [Enterprise](https://docs.litellm.ai/docs/enterprise) |
| Version changes and precise implementation | [Releases](https://github.com/BerriAI/litellm/releases), [source](https://github.com/BerriAI/litellm) |

## AWS implementation references

- [AWS LiteLLM/Bedrock CDK sample](https://github.com/aws-samples/sample-claude-code-with-litellm-and-bedrock):
  TypeScript CDK, container/config and client examples. Useful for task-role and
  runtime wiring. It is explicitly a demonstration requiring hardening; do not
  copy its ingress, sizes, client choice or moving image tags as defaults.
- [AWS Codex/ECS walkthrough](https://aws.amazon.com/blogs/machine-learning/set-up-openai-chatgpt-codex-with-litellm-on-amazon-ecs-and-amazon-bedrock/):
  useful when testing the Responses API and later client integration. It does
  not establish compatibility for another coding client or production capacity.
- [Official AWS Terraform implementation](https://github.com/BerriAI/litellm/tree/main/terraform/litellm/aws):
  inspect as an infrastructure/runtime reference when using CDK; translate the
  required contracts into existing constructs rather than replacing the toolchain.
- [ECS task roles](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task-iam-roles.html)
  and [execution roles](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task_execution_IAM_role.html):
  distinguish application permissions from ECS agent startup operations.
- [ALB attributes](https://docs.aws.amazon.com/elasticloadbalancing/latest/application/edit-load-balancer-attributes.html)
  and [ECS connection draining](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/load-balancer-connection-draining.html):
  inspect the full streaming/shutdown path rather than raising one timeout.

## Refresh method

Record the exact release/image and API surface. Read changes across the upgrade
span, inspect matching schemas/CLI/extension contracts, reproduce startup in an
isolated environment, then run the relevant synthetic request and policy tests.
Update only demonstrated changes in these references. Do not record credentials,
account identifiers, private project routes or incident narratives in this skill.
