---
name: litellm
description: Use when developing, configuring, deploying, reviewing, or troubleshooting LiteLLM Python SDK usage or an LLM gateway/OpenAI-compatible proxy, including local development, routing, Bedrock, ECS/Fargate, CDK, virtual keys, budgets, spend tracking, OpenTelemetry, Prisma migrations, and upgrades.
metadata:
  author: "chearmstrong"
  canonical-source: "https://github.com/chearmstrong/skills"
---

# LiteLLM

Help build and operate LiteLLM with practical development workflows, examples,
deployment patterns, and evidence-backed advice. Cover the gateway and SDK;
leave coding-client design and repository conventions to their own guidance.

## Establish the working context

- Read the repository instructions, deployment design, configuration ownership,
  and relevant implementation before proposing changes. Preserve the chosen
  platform and existing delivery workflow.
- Identify proxy versus in-process SDK, image/package version, OSS versus
  Enterprise, provider/model/region, client API, and persistent dependencies.
  Ask only for missing choices that materially affect the current task.
- LiteLLM supports a monolithic proxy image and a split gateway/backend/UI
  deployment. Confirm which runtime layout the selected release and design use.
- Use the installed release's CLI, schemas, source, and matching upstream docs
  for version-sensitive settings. This skill is a guide, not a pinned product
  specification. Never select models, regions, licences, or credentials by guess.

## NEVER

- Change or lose `LITELLM_SALT_KEY` after storing provider credentials: they become unreadable.
- Edit YAML without checking whether database-managed settings override it.
- Test model access or budgets with the master key; use the intended restricted identity.
- Put Bedrock invocation permissions on the ECS execution role; use the task role.
- Treat readiness, recorded spend, or CDK synth as proof of access or budget enforcement.
- Let several serving tasks run schema migrations; run one controlled migration job.
- Use provider-calling health checks as frequent liveness probes.
- Assume `curl` exists in the chosen image when defining container health checks.

## Choose the relevant reference

| Task | Read |
| --- | --- |
| Run locally, prepare config, exercise a client | [Local development](references/local-development.md) |
| Define ECS/CDK resources, deliver config, migrate or roll out | [ECS and CDK patterns](references/ecs-cdk.md) |
| Configure proxy auth, routing, budgets or telemetry | [Configuration and integrations](references/configuration.md) |
| Use Python calls or Router, handle parameters, retries, errors or cost | [Python SDK patterns](references/python-sdk.md) |
| Diagnose startup, request, streaming or accounting failures | [Troubleshooting and verification](references/verification.md) |
| Find current primary docs or reference implementations | [Source map](references/sources.md) |

Read only the sections needed. Leave other references unloaded until the task
crosses their boundary or they are needed to confirm version-sensitive behaviour.
For local-only or SDK-only tasks, do not load `ecs-cdk.md`. For proxy-only tasks,
skip `python-sdk.md` unless writing an in-process extension or diagnosing SDK behaviour.
For CDK authoring or AWS inspection, also use
the corresponding installed skills when available; these references explain
the LiteLLM integration rather than replacing general AWS guidance.

## Apply and verify

- Keep local tests on the deployed release and the client's actual API surface.
  A Chat Completions smoke test does not establish Responses API compatibility.
- Diagnose the failing step: config resolution, identity, model permission,
  provider request, stream delivery, or accounting. Use the claim-to-evidence
  table in the verification reference to choose the next check.
- Inspect callbacks, spend logs and debug paths for prompt, response, file-content
  and authentication-token capture. Token counts, latency and spend can remain
  useful metadata without capturing request content.
